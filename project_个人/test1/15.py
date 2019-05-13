# -*- coding: utf-8 -*-

from __future__ import absolute_import

import importlib
import traceback
import logging
import json
import re

from six import iteritems

from utils import WorkerPool
import settings

logger = logging.getLogger(__name__)

MESSAGE_MATCHER = re.compile(r'^(@.*?\:?)\s(.*)', re.MULTILINE | re.DOTALL)
# BOT_ICON = settings.BOT_ICON if hasattr(settings, 'BOT_ICON') else None
# BOT_EMOJI = settings.BOT_EMOJI if hasattr(settings, 'BOT_EMOJI') else None


class MessageDispatcher(object):
    def __init__(self, client, plugins):
        self._client = client
        self._pool = WorkerPool(self.dispatch_msg, settings.WORKERS_NUM)
        self._plugins = plugins
        self._channel_info = {}
        self.event = None

    def start(self):
        self._pool.start()

    @staticmethod
    def get_message(msg):
        return msg.get('data', {}).get('post', {}).get('message', '').strip()

    @staticmethod
    def get_sender(msg):
        return msg.get('data', {}).get('sender_name', '').strip()

    def ignore(self, _msg):
        return self._ignore_notifies(_msg) or self._ignore_sender(_msg)

    def _ignore_notifies(self, _msg):
        # ignore message containing specified item, such as "@all"
        msg = self.get_message(_msg)
        return True if any(
            item in msg for item in settings.IGNORE_NOTIFIES) else False

    def _ignore_sender(self, _msg):
        # ignore message from senders specified in settings
        sender_name = self.get_sender(_msg)
        return True if sender_name.lower() in (
            name.lower() for name in settings.IGNORE_USERS) else False

    def is_mentioned(self, msg):
        mentions = msg.get('data', {}).get('mentions', [])
        return self._client.user['id'] in mentions

    def is_personal(self, msg):
        try:
            channel_id = msg['data']['post']['channel_id']
            if channel_id in self._channel_info:
                channel_type = self._channel_info[channel_id]
            else:
                channel = self._client.api.channel(channel_id)
                channel_type = channel['channel']['type']
                self._channel_info[channel_id] = channel_type
            return channel_type == 'D'
        except KeyError:
            logger.info('Once time workpool exception caused by \
                         bot [added to/leave] [team/channel].')
            return False

    def dispatch_msg(self, msg):
        category = msg[0]
        msg = msg[1]
        text = self.get_message(msg)
        responded = False
        msg['message_type'] = '?'
        if self.is_personal(msg):
            msg['message_type'] = 'D'

        for func, args in self._plugins.get_plugins(category, text):
            if func:
                responded = True
                try:
                    func(Message(self._client, msg, self._pool), *args)
                except Exception as err:
                    logger.exception(err)
                    #reply = '[%s] I have problem when handling "%s"\n' % (
                    #    func.__name__, text)
                    #reply += '```\n%s\n```' % traceback.format_exc()
                    reply = '小bot累了~先让它喘口气吧！~'
                    self._client.channel_msg(
                        msg['data']['post']['channel_id'], reply)

        if not responded and category == 'respond_to':
            if settings.DEFAULT_REPLY_MODULE is not None:
                mod = importlib.import_module(settings.DEFAULT_REPLY_MODULE)
                if hasattr(mod, 'default_reply'):
                    return getattr(mod, 'default_reply')(self, msg)
            self._default_reply(msg)

    def _on_new_message(self, msg):
        if self.ignore(msg) is True:
            return

        msg = self.filter_text(msg)
        if self.is_mentioned(msg) or self.is_personal(msg):
            self._pool.add_task(('respond_to', msg))
        else:
            self._pool.add_task(('listen_to', msg))


#################message_matcher#########################
    def filter_text(self, msg):
        text = self.get_message(msg)
        if self.is_mentioned(msg):
            m = MESSAGE_MATCHER.match(text)
            if m:
                msg['data']['post']['message'] = m.group(2).strip()
        return msg

    def load_json(self):
        for item in ['post', 'mentions']:
            if self.event.get('data', {}).get(item):
                self.event['data'][item] = json.loads(
                    self.event['data'][item])

    def loop(self):
        for self.event in \
            self._client.messages(True, ['posted', 'added_to_team',
                                         'leave_team', 'user_added',
                                         'user_removed']):
            if self.event:
                self.load_json()
                self._on_new_message(self.event)

    def _default_reply(self, msg):
        if settings.DEFAULT_REPLY:
            return self._client.channel_msg(
                msg['data']['post']['channel_id'], settings.DEFAULT_REPLY)

        default_reply = [
            u'小bot累了~先让它喘口气吧！~'
            #u'Bad command "%s", Here is what I currently know '
            #u'how to do:\n' % self.get_message(msg),
        ]

        # create dictionary organizing commands by plugin
        modules = {}
        for p, v in iteritems(self._plugins.commands['respond_to']):
            key = v.__module__.title()
            if key not in modules:
                modules[key] = []
            modules[key].append((p.regex.pattern, v.__doc__))

        if settings.PLUGINS_ONLY_DOC_STRING:
            docs_fmt = u'\t{1}'
        else:
            docs_fmt = u'\t`{0}` - {1}'

        for module, commands in modules.items():
            #default_reply += [u'Plugin: **{}**'.format(module)]
            commands.sort(key=lambda x: x[0])
           # for pattern, description in commands:
           #     default_reply += [docs_fmt.format(pattern, description)]

        self._client.channel_msg(
            msg['data']['post']['channel_id'], '\n'.join(default_reply))

