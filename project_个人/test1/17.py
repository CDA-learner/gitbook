import copy
import json
import re


# MESSAGE_MATCHER = re.compile(r'^(@.*?\:?)\s(.*)', re.MULTILINE | re.DOTALL)
msg={'event': 'posted', 'data': {'channel_display_name': '@jane', 'channel_name': 'a4omki79apnd8xus8hfmr1j9ow__f4rkcpzqh3rydxrwgnmn8eemtr', 'channel_type': 'D', 'mentions': '["f4rkcpzqh3rydxrwgnmn8eemtr"]', 'post': '{"id":"dk3b94imwfdutcu5hi7qjfoe1y","create_at":1555727497813,"update_at":1555727497813,"edit_at":0,"delete_at":0,"is_pinned":false,"user_id":"a4omki79apnd8xus8hfmr1j9ow","channel_id":"oou1mcokwtn4zfr7a7wkhw61xo","root_id":"","parent_id":"","original_id":"","message":"@ibot restart 二人牛牛-测试\\n@ibot  restart 飞禽走兽-测试","type":"","props":{},"hashtags":"","pending_post_id":"a4omki79apnd8xus8hfmr1j9ow:1555727497378","metadata":{}}', 'sender_name': 'jane', 'team_id': ''}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': 'oou1mcokwtn4zfr7a7wkhw61xo', 'team_id': ''}, 'seq': 2}
# message_1 = json.loads(msg['data']['post'])['message'].split('@')[1:]
# t = copy.deepcopy(msg)
# for i in range(len(message_1)):
#     json.loads(msg['data']['post'])['message'] = message_1[i]
#     print(t)

j=0
def load_json(msg):
    for item in ['post', 'mentions']:
        if msg.get('data', {}).get(item):
            msg['data'][item] = json.loads(
                msg['data'][item])
            message_1 = msg['data']['post']['message'].split('@')[1:]
            t = copy.deepcopy(msg)
            for i in range(len(message_1)):
                t['data']['post']['message'] = '@'+message_1[i].strip()
                yield t


load_json(msg)