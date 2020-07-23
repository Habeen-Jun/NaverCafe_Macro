
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
import time 
# from main import MyWindow


# Qtdesigner로 생성한 ui불러옴 
login_class = uic.loadUiType("login.ui")[0]

class LoginWindow(QMainWindow, login_class):

    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_check)

    def login_check(self):
        ID = self.lineEdit.text()
        PW = self.lineEdit_2.text()

        if ID == '':
            QMessageBox.information(self,'alert','아이디를 입력해주세요!')
        elif PW == '':
            QMessageBox.information(self,'alert','비밀번호를 입력해주세요!')
        else:
            conn = sqlite3.connect('login.db')
            result = conn.execute('select * from users where id = ? and pw = ?',(ID,PW))
            if len(result.fetchall()) > 0:
                QMessageBox.information(self, 'congrats','로그인 성공!')
                self.switch_window.emit()
                
            else: 
                QMessageBox.information(self, 'alert','아이디와 패스워드를 확인해주세요')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()
