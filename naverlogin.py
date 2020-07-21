
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
import time 
from naverposting import Naver_Posting
# from main import MyWindow


# Qtdesigner로 생성한 ui불러옴 
login_class = uic.loadUiType("naverlogin.ui")[0]


class LoginWindow(QMainWindow, login_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.loginproccess)
    def loginproccess(self):
        ID = self.lineEdit.text()
        PW = self.lineEdit_2.text()

        if ID == '':
            QMessageBox.information(self,'alert','아이디를 입력해주세요')
        elif PW == '':
            QMessageBox.information(self,'alert','패스워드를 입력해주세요')
        else:
            try:
                self.naver = Naver_Posting(self,ID,PW)
                # self.naver = threading.Thread(target=Naver_Posting, args=(self,ID,PW)).start()
                print(type(self.naver))
                # self.naver = threading.Thread(target=Naver_Posting(self,ID,PW)).start()
                # self.set_category()
                QMessageBox.information(self,'congrats','로그인 성공')
                self.login_OK = True
            except:
                QMessageBox.information(self,'alert','로그인 실패')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()
    # myWindow.naver.driver.close()
    # kill_process('chromedriver')
app = QApplication(sys.argv)
myWindow = LoginWindow()
myWindow.show()
app.exec_()