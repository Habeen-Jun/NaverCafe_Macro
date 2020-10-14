from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt, QUrl
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from dbmodel import dbmodel
import time 
from path_manager import resource_path
# Qtdesigner로 생성한 ui불러옴 
form_class = uic.loadUiType(resource_path("./ui_files/editwindow.ui"))[0]
        
class Editwindow(QWidget, form_class):

    finished_Editing = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.openimagefile)
        self.pushButton.clicked.connect(self.update_post)
        self.lineEdit_5.setReadOnly(True)

    def keyPressEvent(self, e):
        print('keypressed')
        
    def openimagefile(self):
        """
        대표이미지 파일 설정
        """
        fname = QFileDialog.getOpenFileName(self)
        self.lineEdit_5.setText(fname[0])


    def getFormattedCurrentTime(self):
        now = time.localtime()
        c_time =  "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        return c_time

    def setID(self,ID):
        self.id = ID 


    def update_post(self):
        """
        게시글 수정
        """
        
        title = self.lineEdit_2.text().replace('\n','')
        price = self.lineEdit_3.text().replace('\n','')
        contents = self.textEdit.toHtml()
        cateURL = self.lineEdit_4.text().replace('\n','').lstrip().rstrip()
        tag = self.lineEdit.text()
        image = self.lineEdit_5.text()
        cafe_address = self.lineEdit_6.text().replace('\n','')

        if title == '':
            QMessageBox.information(self,'Alert!!','제목은 필수항목입니다.')
        elif cafe_address == '':
            QMessageBox.information(self,'Alert!!','카페주소는 필수항목입니다.')
        elif contents == '':
            QMessageBox.information(self,'Alert!!','내용은 필수항목입니다.')
        elif cateURL == '0':
            QMessageBox.information(self,"Alert!!", '게시판을 선택해주세요.')
        elif image == '':
            QMessageBox.information(self,"Alert!", '대표이미지는 필수항목입니다.')
        elif price == '':
            QMessageBox.information(self,'Alert!','판매가는 필수항목입니다.')
        elif price != '':
            try:
                int(price)
            except:
                QMessageBox.information(self, "Alert!",'판매가는 숫자로 입력해 주세요')
            else:
                print('editing post')
                c_time = self.getFormattedCurrentTime()

                data = {

                    'time':c_time,
                    'title':title,
                    'price':price,
                    'body':contents,
                    'category': cateURL,
                    'tag': tag,
                    'img': image,
                    'id': self.id, #게시물 ID 
                    'cafe_address': cafe_address,
                }

                dbconn = dbmodel()
                dbconn.update_item(data)
                QMessageBox.information(self,'','게시물이 수정되었습니다')
                self.finished_Editing.emit()
                self.close()


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()