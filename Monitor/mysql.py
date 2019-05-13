import pymysql
import config

connection = pymysql.connect(**config.MYSQL_CONFIG)

result = None

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tb_server")
        result = cursor.fetchall()
finally:
    connection.close()
    connection = None

def getResult():
    return result
