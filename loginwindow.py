
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
# from main import MyWindow


# Qtdesigner로 생성한 ui불러옴 
login_class = uic.loadUiType("login.ui")[0]

class LoginWindow(QMainWindow, login_class):

    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_check)
        self.lineEdit_2.returnPressed.connect(self.login_check)
        self.lineEdit.setPlaceholderText('ID')
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
            conn = pymysql.connect(host='database-1.ccjfvjnmfvc8.us-east-1.rds.amazonaws.com',port=3306, user='admin', passwd='jih4412*', db='rs_member')
            curs = conn.cursor()
            curs.execute('select * from user where ID = %s and PW = %s',(ID,PW))
            result = curs.fetchall()
            if len(result) > 0:
                expired_date = result[0][5]
                today = datetime.today()
                if expired_date > today:
                    remaining_days = (expired_date-today).days
                    QMessageBox.information(self, 'congrats','로그인 성공! \n남은 기간: %s일' % str(remaining_days))
                    self.switch_window.emit()
                else:
                    QMessageBox.information(self, 'EXPIRED','회원님의 이용기간이 만료되었습니다 \n사용 연장 신청을 원하시면 리얼셀러에 문의해 주세요.')
            else: 
                QMessageBox.information(self, 'alert','아이디와 패스워드를 확인해주세요')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()
