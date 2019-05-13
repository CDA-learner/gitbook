#! usr/bin/env python
# _*_ coding:utf-8_*_

import os
import glob

"""
自动化脚本初始安装环境配置

"""
from searchdir import search

def init_config():
    x = search("E:\运维", "requirements.txt")
    for m in x:
        print(m)
        cmd = 'pip install -r ' + m
        print(cmd)
        text_list = os.popen(cmd).readlines()
        for line in text_list:
                print(line)


if __name__ == '__main__':
    init_config()