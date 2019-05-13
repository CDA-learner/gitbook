# coding:utf-8

"""
python 查找文件模块，
也可以换成操作linux 命令来执行
"""

import os

m = []

def search(path, word):
    for dirpath,dirnames,filenames in os.walk(path):
        for filename in filenames:
            if word in filename:
                m.append(os.path.join(dirpath, filename))

    return m



