#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import string
import random
import argparse
import subprocess
import requests
import json
import uuid
import md5
import oss2
from datetime import datetime

class opsaliyunoss(object):
        def __init__(self):
                pass

        def connect_aliyun_oss(self, access_key_id, access_key_secret, bucket_name, endpoint):
                bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
                return bucket

        def aliyun_put_object(self, bucket, local_file_name, remote_file_name, file_meta):
                with open(local_file_name, 'rb') as fileobj:
                        result = bucket.put_object(remote_file_name, fileobj, headers={'Content-Type': 'text/xml'})
                if result.status == 200:
                    return_msg = '{0},{1}'.format(file_meta, 'https://img.carfree.net/'+remote_file_name)
                    return return_msg
                else:
                    print(local_file_name+' upload failed!')

        def aliyun_http_put_object(self, bucket, fileobj, remote_file_name, file_meta):
                result = bucket.put_object(remote_file_name, fileobj, headers={'Content-Type': 'text/xml'})
                if result.status == 200:
                        return_msg = '{0},{1}'.format(file_meta, 'https://img.carfree.net/'+remote_file_name)
                        return return_msg
                else:
                        print(local_file_name+' upload failed!')

        def gen_token(self):
            return ''.join(random.choice(string.ascii_letters+string.digits) for x in range(15))

        def get_remote_file_name(self,bucket_dir, local_file_name):
                daymd5 = md5.new(datetime.now().strftime('%Y%m%d')).hexdigest()
                pre_dir = bucket_dir + "/" + daymd5[0:2] + "/" + daymd5[2:4] + "/"

                fileext = os.path.splitext(local_file_name)[1]
                x = self.gen_token()
                return pre_dir + x + fileext
