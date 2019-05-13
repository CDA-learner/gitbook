# coding:utf-8

import random
import time
import _thread


def creat_random():
    count =0
    while count < 30:
        x = random.randint(0,100)
        print('结果%s '%x)
        count += 1

try:
    _thread.start_new_thread(creat_random, ( ))
    _thread.start_new_thread(creat_random, ( ))
except :
    print('error')

while 1:
   pass






