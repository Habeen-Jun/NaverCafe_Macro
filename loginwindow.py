
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
import time 
import pymysql
from datetime import datetime
from check_alive import check_login
import threading
from check_alive import check_alive
import socket
# from main import MyWindow
from path_manager import resource_path

# Qtdesigner로 생성한 ui불러옴 
login_class = uic.loadUiType(resource_path("login.ui"))[0]

class LoginWindow(QMainWindow, login_class):

    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_check)
        self.lineEdit_2.returnPressed.connect(self.login_check)
        self.lineEdit.setPlaceholderText('ID')
        self.textEdit.setReadOnly(True)
        self.get_info()
        self.lineEdit_3.setReadOnly(True)
        PW = self.lineEdit_2
        PW.setEchoMode(QLineEdit.Password)
        PW.setPlaceholderText('password')

    def login_check(self):
        ID = self.lineEdit.text()
        PW = self.lineEdit_2.text()
        

        if ID == '':
            QMessageBox.information(self,'alert','아이디를 입력해주세요!')
        elif PW == '':
            QMessageBox.information(self,'alert','비밀번호를 입력해주세요!')
        else:
            conn = pymysql.connect(host='database-1.cnc8bpjvdf5m.us-east-2.rds.amazonaws.com',port=3306, user='admin', passwd='wjsgkqls123', db='rs_member', cursorclass=pymysql.cursors.DictCursor)
            
            curs = conn.cursor()
            curs.execute('select * from user where ID = %s and PW = %s',(ID,PW))
            result = curs.fetchall()
            conn.close()
            print(result)
            if len(result) > 0:
                result =result[0]
                registered_devices = [result['device1'],result['device2'],result['device3']]
                registered_devices = [str(dev).replace('-',':') for dev in registered_devices]
                login_ok = check_login(ID,PW)
                if login_ok:
                    expired_date = result['expired_date']
                    today = datetime.today()
                    print(registered_devices)
                    print(self.getMac())
                    if self.getMac() in registered_devices:
                        if expired_date > today:
                            remaining_days = (expired_date-today).days
                            QMessageBox.information(self, 'congrats','로그인 성공!\n 접속 디바이스: %s\n남은 기간: %s일' % (self.getMac(),str(remaining_days)))
                            self.check_login()
                            self.switch_window.emit()
                        else:
                            QMessageBox.information(self, 'EXPIRED','회원님의 이용기간이 만료되었습니다 \n사용 연장 신청을 원하시면 개발자에게 문의해 주세요.')
                    else:
                        QMessageBox.information(self, 'NOT REGISTERED','등록되지 않은 기기입니다 \n 현재 기기: {}'.format(self.getMac()))
                else:
                    QMessageBox.information(self, 'alert','프로그램이 이미 실행 중입니다.')
            else: 
                QMessageBox.information(self, 'alert','아이디와 패스워드를 확인해주세요')
            

    def get_info(self):
        conn = pymysql.connect(host='database-1.cnc8bpjvdf5m.us-east-2.rds.amazonaws.com',port=3306, user='admin', passwd='wjsgkqls123', db='rs_member')
        curs = conn.cursor()
        curs.execute('select * from announcement')
        result = curs.fetchall()[0][0]
        self.textEdit.append(result)
        
    def check_login(self):
        ID = self.lineEdit.text()
        PW = self.lineEdit_2.text()
        t = threading.Thread(target=check_alive, args=(ID,PW))
        t.setDaemon(True)
        t.start()
    
    def ipcheck(self):
        return socket.gethostbyname(socket.getfqdn())
    def getMac(self):
        import getmac
        return getmac.get_mac_address().upper() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()
    
