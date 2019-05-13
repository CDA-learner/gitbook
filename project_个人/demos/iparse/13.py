# x={"199002":["jk-888.com","www-jk888.com","jk888.app","jk888.co","jk678.com","jk888.com"]}
# print(x.keys())

# coding :utf-8

import requests
import json
import re
import os

keys='36979'
name ='huihuang200.com'
conf_path = 'C:/Users/admin/Desktop/'

with open(os.path.join(conf_path,'template.conf'), 'r', encoding='utf-8') as f:
    temp_tex = "".join(f.readlines())
    f.close()
confg_tex = temp_tex.replace('SERVER_NAME',name).replace('SERVER_KEY',keys)
try:
    with open(os.path.join(conf_path, keys+'.conf'),'w') as f1:
        f1.write(confg_tex)
        f1.close()
except IOError:
     file= open(os.path.join(conf_path, keys+'.conf'), 'r')


