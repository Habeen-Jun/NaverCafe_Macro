import pymysql
from datetime import datetime, timedelta

reg_date = datetime.today()
expired_date = reg_date + timedelta(days=30)


expired_date = expired_date.strftime("%Y-%m-%d")
reg_date = reg_date.strftime("%Y-%m-%d") 



conn = pymysql.connect(host='database-1.ccjfvjnmfvc8.us-east-1.rds.amazonaws.com',port=3306, user='admin', passwd='jih4412*', db='rs_member')
curs = conn.cursor()
sql = """insert into user(name, ID, PW, reg_date , expired_date) values(%s, %s, %s, %s, %s)"""
curs.execute(sql, ('전하빈','junhabeen','wjsgkqs123',reg_date, expired_date))
conn.commit()
conn.close()
