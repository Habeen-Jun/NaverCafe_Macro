import pymysql
import threading
import time 


def check_alive(ID,PW):
    while True:
        conn = pymysql.connect(host='database-1.cnc8bpjvdf5m.us-east-2.rds.amazonaws.com',port=3306, user='admin', passwd='wjsgkqls123', db='rs_member')
        curs = conn.cursor()
        curs.execute('update user set last_active_sign = now() where ID = %s and PW = %s',(ID,PW))
        conn.commit()
        conn.close()
        print('signal sent')
        time.sleep(30)
        

# check_alive('junhabeen','wjsgkqls123')

def check_login(ID,PW):
    conn = pymysql.connect(host='database-1.cnc8bpjvdf5m.us-east-2.rds.amazonaws.com',port=3306, user='admin', passwd='wjsgkqls123', db='rs_member')
    curs = conn.cursor()
    # 마지막 로그인 시간 구하기 
    curs.execute('select last_active_sign from user where ID = %s and PW = %s',(ID,PW))
    last_login_time = curs.fetchall()[0][0]
    # 서버 현재 시간 구하기 
    curs.execute('select now()')
    c_time = curs.fetchall()[0][0]
    conn.commit()
    conn.close()
    if last_login_time != None:
        # 1분 넘으면 True, 아니면 False
        check_over_1_min = (c_time - last_login_time).seconds >= 60
        # 마지막 시그널 1분 지나면 로그인 가능 
        if check_over_1_min:
            # print('로그인 가능')
            return True
        else:
            # print('로그인 불가')
            return False
    else:
        # 최초접속
        return True
    try:
        conn = pymysql.connect(host='database-1.cnc8bpjvdf5m.us-east-2.rds.amazonaws.com',port=3306, user='admin', passwd='wjsgkqls123', db='rs_member')
        curs = conn.cursor()
        # 마지막 로그인 시간 구하기 
        curs.execute('select last_active_sign from user where ID = %s and PW = %s',(ID,PW))
        last_login_time = curs.fetchall()[0][0]
        # 서버 현재 시간 구하기 
        curs.execute('select now()')
        c_time = curs.fetchall()[0][0]
        conn.commit()
        conn.close()
        if last_login_time != None:
            # 1분 넘으면 True, 아니면 False
            check_over_1_min = (c_time - last_login_time).seconds >= 60
            # 마지막 시그널 1분 지나면 로그인 가능 
            if check_over_1_min:
                # print('로그인 가능')
                return True
            else:
                # print('로그인 불가')
                return False
        else:
            # 최초접속
            return True
    except:
        # print('로그인 정보 틀림')
        return False
  
    
if __name__ == '__main__':
    t = threading.Thread(target=check_alive, args=('junhabeen','wjsgkqls123'))
    t.start()
    check_login('junhabeen','wjsgkqls123')
