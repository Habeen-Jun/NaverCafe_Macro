
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import time 
from naverlogin import Naverlogin
import threading
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from PyQt5.QtWidgets import QDialog



# Qtdesigner로 생성한 ui불러옴 
login_class = uic.loadUiType("naverlogin.ui")[0]


class NaverLoginWindow(QMainWindow, login_class):
    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.loginproccess)
        self.login_OK = False
        self.lineEdit.setFocus(True)
        # 엔터 누르면 로그인 
        self.lineEdit_2.returnPressed.connect(self.loginproccess)

    def keyPressEvent(self, event):           
        if event.key() == Qt.Key_Tab:
            self.lineEdit_2.setFocus(True)

    def loginproccess(self):
        ID = self.lineEdit.text()
        PW = self.lineEdit_2.text()

        if ID == '':
            QMessageBox.information(self,'alert','아이디를 입력해주세요')
        elif PW == '':
            QMessageBox.information(self,'alert','패스워드를 입력해주세요')
        else:
            try:
                self.t = Naverlogin()
                self.t.set_ID(ID)
                self.t.set_PW(PW)
                self.t.start()
                self.t.finished.connect(self.change_to_main)
                # 스레드 끝날때까지 기다림..
                while not self.t.isFinished():
                    pass
                self.ID = ID
                self.PW = PW
                QMessageBox.information(self, 'congrats','로그인 성공')
            except:
                QMessageBox.information(self, 'alert','로그인 실패')
            
    def toMainWindow(self):
        self.switch_window.emit()
        print('메인 윈도우로~')

    @pyqtSlot(object,str,str)
    def change_to_main(self,driver,ID,PW):
        self.driver = driver
        self.ID = ID
        self.PW = PW
        self.toMainWindow()
        
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = NaverLoginWindow()
    mywindow.show()
    app.exec_()
