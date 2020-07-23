
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
import time 
from naverposting import Naver_Posting
import threading



# Qtdesigner로 생성한 ui불러옴 
login_class = uic.loadUiType("naverlogin.ui")[0]


class NaverLoginWindow(QMainWindow, login_class):
    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.loginproccess)
        self.login_OK = False

    def loginproccess(self):
        # ID = self.lineEdit.text()
        # PW = self.lineEdit_2.text()

        # if ID == '':
        #     QMessageBox.information(self,'alert','아이디를 입력해주세요')
        # elif PW == '':
        #     QMessageBox.information(self,'alert','패스워드를 입력해주세요')
        # else:
        #     self.naver = Naver_Posting(self,ID,PW)
        #     driver = self.naver.driver
        #     self.category_list = self.naver.category_list
        #     print(driver)
        #     print(self.category_list)
            # t = threading.Thread(target=Naver_Posting, args=(self,ID,PW))
            # t.start()
            # print(type(self.naver))
            # self.naver = threading.Thread(target=Naver_Posting(self,ID,PW)).start()
            # self.set_category()
            # t.join()
            QMessageBox.information(self,'congrats','로그인 성공')
            self.login_OK = True
            self.toMainWindow()
            # self.hide()


            # import main
            # app = QApplication(sys.argv)
            # myWindow = MyWindow()
            # myWindow.show()
            # app.exec_()
            # try:
            #     # self.naver = Naver_Posting(self,ID,PW)
            #     self.naver = threading.Thread(target=Naver_Posting, args=(self,ID,PW)).start()
            #     print(type(self.naver))
            #     # self.naver = threading.Thread(target=Naver_Posting(self,ID,PW)).start()
            #     # self.set_category()
            #     QMessageBox.information(self,'congrats','로그인 성공')
            #     self.login_OK = True
            #     self.hide()
            #     import main
            # except:
            #     QMessageBox.information(self,'alert','로그인 실패')
    def toMainWindow(self):
        # sys.exit()
        # QCoreApplication.instance().quit
        # self.close()
        
        # import main
        # app1 = QApplication(sys.argv)
        # mywindow = MyWindow()
        # mywindow.show()
        # app1.exec_()
        self.switch_window.emit()
        # win = MyWindow()
        # win.showModal()
        print('메인 윈도우로~')
        # self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = NaverLoginWindow()
    mywindow.show()
    app.exec_()
    
    
    # myWindow.naver.driver.close()
    # kill_process('chromedriver')
