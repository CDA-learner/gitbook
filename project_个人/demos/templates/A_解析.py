# encoding:utf-8

import requests
import json
import dns.resolver
import sys


# 通过域名获取域名的A记录
def GetArecordIp(domain_name):
    address = []
    try:
        host_a = dns.resolver.query(domain_name, 'A')
        for i in host_a.response.answer:
            for j in i.items:
                address.append(j.address)
        return address
    except:
        return False


# 通过调用淘宝的api根据ip获取城市
def get_city(ip_addr):
    ip = ip_addr
    # 通过淘宝的api查询ip信息
    req = requests.get("http://ip.taobao.com/service/getIpInfo.php?ip={}".format(ip))
    if req:
        ip_data = json.loads(req.content)
        ip_address = ip_data['data']

        are = ''.join([ip_address['country'], ip_address['area'], ip_address['city']])
        json.dumps(are)
        # print are
        return are


def write_to_html(domain_ip):
    # 通过拼凑ip和域名最终形成网页信息
    # print domain_ip
    title = "域名解析信息"
    tbody = ''
    for domain, ipcity in domain_ip.items():
        print (domain, ipcity[0][0], ipcity[0][1], ipcity[1][0], ipcity[1][1])
        tbody += '<tr>\n<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>\n<tr>\n' % (
        domain, ipcity[0][0], ipcity[0][1], ipcity[1][0], ipcity[1][1])

    html_tpl = '''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
        </head>
        <body>
            <table border="1" cellspacing="0" cellpadding="0" color='pink'>
                <thead>
                    <tr cellspacing="0" cellpadding="0">
                        <th>域名</th>
                        <th>ip信息1</th>
                        <th>ip所在城市1</th>
                        <th>ip信息2</th>
                        <th>ip所在城市2</th>
                    </tr>
                </thead>
                {tbody}
            </table>
        </body>
    </html>
    '''
    html_handle = open('domain01.html', 'w')
    html_handle.write(html_tpl.format(title=title, tbody=tbody))
    html_handle.close()


# 根据域名列表获取ip地址
def main(domain_file):
    f = open(domain_file, 'r')
    domain_list = f.readlines()
    f.close()

    domain_ip = {}
    for domain in domain_list:
        domain_name = domain.rstrip()
        ip_list = GetArecordIp(domain_name)
        ip_city_list = []

        # ip 不为空则处理
        if ip_list:
            for i in ip_list:
                city = get_city(i)
                ip_city = [i, city]
                ip_city_list.append(ip_city)
            # print json.dumps(ip_city_list).decode("unicode-escape")
            # ip=','.join(str(i)for i in ip_city_list)
            # json.dumps(ip_city_list).decode("unicode-escape")可以转为中文显示
            domain_ip[domain_name] = ip_city_list
            # print domain_name,json.dumps(ip_city_list).decode("unicode-escape")
        else:
            print
            "%s has no record" % domain_name

    # 将信息写入网页
    write_to_html(domain_ip)


if __name__ == '__main__':
    domain_file = "C:/Users/admin/Desktop/domain.txt"
    main(domain_file)
