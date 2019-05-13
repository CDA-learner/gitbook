#!coding:utf-8
import json
import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta

class CJsonEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj.__class__, DeclarativeMeta):                 ##将数据库对象转化成字典
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x!='password']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:  
            return json.JSONEncoder.default(self, obj)