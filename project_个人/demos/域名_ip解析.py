# coding:utf-8

import os, sys
from socket import gethostbyname
import socket

def main():
    # domain.txt里面存储的是需要批量解析的域名列表，一行一个
    with open('C:/Users/admin/Desktop/domain.txt', 'r') as f:
        for line in f.readlines():
            try:
                host = gethostbyname(line.strip('\n'))
            except Exception as e:
                print
                e
            else:
                # result.txt里面存储的是批量解析后的结果
                with open('result.txt', 'a+') as r:
                    r.write(line.strip('\n') + ' ')
                    r.write(host + '\n')


if __name__ == '__main__':
    main()