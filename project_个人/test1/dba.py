#! usr/bin/env python
# coding:utf-8


import pymysql

conn = pymysql.connect(host='172.20.100.149', port=3306, user='test-user', password='test-User123456',
                       db='micro_account')
cursr = conn.cursor()


def get_new(par_id):
    sql="""insert into account_to_user (select f.id,f.site_id,IFNULL(SUM(CAST(f.amount as decimal(18,2))),0) as amount from(
        select t.id,t.account,IFNULL(SUM(CAST(a.amount as decimal(18,2))),0) as amount,a.create_date,a.receipts_type,a.state,t.account_type,a.site_id
        from tb_pay_record as a JOIN tb_acc_account
        as t ON a.account=t.account and a.site_id=t.site_id
        where t.parent_account_id =%s
        or t.parent_account_id in(SELECT id FROM tb_acc_account where parent_account_id = %s)
        or t.parent_account_id in(SELECT id FROM tb_acc_account where parent_account_id in(SELECT id FROM tb_acc_account
        where parent_account_id = %s))
        GROUP BY  a.create_date,a.account
        ) as f where 1=1
        and f.site_id=36979 and f.account_type=2
        and f.state in(2,3) and f.receipts_type!=2);"""%(par_id,par_id,par_id)
    print('执行当前的parent_id为:',par_id)
    cursr.execute(sql)
    conn.commit()
    print('parent_id %s插入account_to_user成功'%par_id)

def get_id():
    lst = []
    sql="""select DISTINCT IFNULL(parent_account_id,0) from  tb_acc_account ; """
    cursr.execute(sql)
    data = cursr.fetchall()
    for item in data :
        if item[0]:
            lst.append(item[0])
    print('读取成功',lst)
    return lst

if __name__ == '__main__':
    ids=get_id()
    for id in ids:
        get_new(id)