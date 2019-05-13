#!/usr/bin/python

import _thread
import time
import pymysql
import threading


exitFlag = 0

def get_new(id,threading_name, Thread_id):
    conn = pymysql.connect(host='172.20.100.252', port=3306, user='usertest', password='123456',
                           db='micro_account')
    cursr = conn.cursor()
    sql = """replace into account_to_user_copy1(id,site_id,money) values(%s,%s,(select IFNULL(SUM(CAST(f.amount as decimal(18,2))),0) as amount from(
                    select t.id,t.account,IFNULL(SUM(CAST(a.amount as decimal(18,2))),0) as amount,a.create_date,a.receipts_type,a.state,t.account_type,t.site_id
                    from tb_pay_record as a JOIN tb_acc_account
                    as t ON a.account=t.account and a.site_id=t.site_id
                    where parent_account_id is not null and t.parent_account_id =%s
                    or t.parent_account_id in(SELECT id FROM tb_acc_account where parent_account_id = %s and parent_account_id is not null)
                    or t.parent_account_id in(SELECT id FROM tb_acc_account where parent_account_id in(SELECT id FROM tb_acc_account
                    where parent_account_id = %s and parent_account_id is not null))
                    GROUP BY  a.create_date,a.account
                    ) as f where 
                    f.account_type=2
                    and f.state in(2,3) and f.receipts_type!=2));""" % (id[0], id[1], id[0], id[0], id[0])
    print('执行当前的parent_id为:', id[0])
    cursr.execute(sql)
    print('开始执行线程', threading_name, Thread_id)
    conn.commit()
    print('parent_id %s插入account_to_user成功' % id[0])


def get_id():
    conn = pymysql.connect(host='172.20.100.252', port=3306, user='usertest', password='123456',
                           db='micro_account')
    cursr = conn.cursor()
    lst = []
    sql = """select id,site_id from  tb_acc_account where parent_account_id is not null and account_type=2; """
    cursr.execute(sql)
    data = cursr.fetchall()
    print('data', data)
    for item in data:
        lst.append(item)
    print('读取成功', lst)
    return lst

lst_1=get_id()

# 创建新线程
for i in range(len(lst_1)):
    thread1 = threading.Thread(target=get_new, args=(lst_1[i],"Thread-1", 1))
    thread2 = threading.Thread(target=get_new, args=(lst_1[i+1],"Thread-2", 2))
    i+=2
    thread1.start()
    thread2.start()
thread1.join()
thread2.join()
print ("退出主线程")