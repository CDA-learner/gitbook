#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import argparse
import subprocess
import requests
import json
import telegram

TELEGRAM_BOT_TOKEN = '839308438:AAFmLwkNGvrCNDnjfWaRzx6GPuI-JB1suh8'


class opstelegrambot(object):
    def __init__(self):
        pass

    def bot(self):
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        return bot

    def send_message(self, channelId, message):
        bot = self.bot()
        bot.send_message(chat_id=channelId, text=message)

    def send_html_message(self, channelId, message):
        bot = self.bot()
        bot.send_message(chat_id=channelId, text=message, parse_mode=telegram.ParseMode.HTML)

    def build_success_msg(self, channelId, message):
        text = '<b>Build successfully</b>\r\n' + message
        self.send_html_message(channelId, text)

    def build_error_msg(self, channelId, message):
        text = '<b>Build ERROR</b>\r\n'
        text += message
        self.send_html_message(channelId, text)
