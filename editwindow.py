from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QUrl
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from dbmodel import dbmodel

# Qtdesigner로 생성한 ui불러옴 
form_class = uic.loadUiType("macro0704.ui")[0]
form_class = uic.loadUiType("editwindow.ui")[0]
        
class Editwindow(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.openimagefile)
        self.pushButton.clicked.connect(self.update_post)


    def openimagefile(self):
        """
        대표이미지 파일 설정
        """
        fname = QFileDialog.getOpenFileName(self)
        self.lineEdit_4.setText(fname[0])
    
    def update_post(self):
        """
        게시글 수정
        """
        dbconn = dbmodel()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()