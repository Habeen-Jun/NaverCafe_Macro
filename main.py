
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
import time 
from dbmodel import dbmodel
from text_to_html import text_to_html
from naverposting import Naver_Posting
import threading
from processkill import kill_process

# Qtdesigner로 생성한 ui불러옴 
form_class = uic.loadUiType("/Users/apple/python/navercafe_macro/macro0704.ui")[0]


class MyThread:
    def job(self,naver,total_interval,interval,option_data, item_list):
        naver.post(interval, option_data, item_list)
        t = threading.Timer(total_interval,self.job, args=(naver,total_interval,interval,option_data,item_list))
        t.start()

def main(naver,total_interval,interval,option_data,item_list):
    mt = MyThread()
    mt.job(naver,total_interval,interval,option_data,item_list)

    
    


        


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.login_OK = False 
        
        self.setupUi(self)
  
        conn = dbmodel()
    
        self.tableWidget = conn.load_data(self.tableWidget)
        
        # 게시글 테이블
        self.tableWidget.setHorizontalHeaderLabels(["등록날짜","제목", "내용", "가격","대표이미지","카테고리",'태그','카페','id','category_id'])
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignRight)
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # edit 금지 모드

        글등록 = self.pushButton_2
        글등록.clicked.connect(self.add_item)

        delete_button = self.pushButton_6
        delete_button.clicked.connect(self.del_item)

        self.pushButton.clicked.connect(self.openimagefile)

        Alldelete = self.pushButton_7
        Alldelete.clicked.connect(self.clear_items)

        self.post_button = self.pushButton_3
        self.post_button.clicked.connect(self.post)

        stop_button = self.pushButton_9
        stop_button.clicked.connect(self.stop_process)

        login_button = self.pushButton_5
        login_button.clicked.connect(self.login_process)

    def login_process(self):
        ID = self.lineEdit_3.text()
        PW = self.lineEdit_10.text()

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
                self.set_category()
                QMessageBox.information(self,'congrats','로그인 성공')
                self.login_OK = True
            except:
                QMessageBox.information(self,'alert','로그인 실패')


    def check_option(self):
        allow_comments = self.checkBox.isChecked()
        alarm_to_all = self.checkBox_2.isChecked()
        searched = self.checkBox_3.isChecked()
        phone_show = self.checkBox_5.isChecked()
        naver_pay = self.checkBox_7.isChecked()
        use_disposable = self.checkBox_6.isChecked()
        allow_rightclick = self.checkBox_4.isChecked()
        keep_update = self.checkBox_9.isChecked()

        option_data = {
            "allow_comments":allow_comments,
            "alarm_to_all":alarm_to_all,
            "searched":searched,
            "phone_show":phone_show,
            "naver_pay":naver_pay,
            "use_disposable": use_disposable,
            "allow_rightclick": allow_rightclick,
            "keep_update":keep_update
            }

        print(option_data)
        return option_data


    def post(self):
        """글등록 데이터 naverposting의 post함수 연결  """
        # 로그인 여부 체크
        ID = self.lineEdit_3.text()
        PW = self.lineEdit_10.text()
        total_interval = 0

        if self.login_OK == False:
            QMessageBox.information(self,"alert",'먼저 로그인 해주세요')
        else:
        #생성자 로그인 창 닫쳤을 경우 네이버 창 재 생성 
            try:
                print('창 있음')
                self.naver
            except AttributeError as e:
                print('네이버 창 다시 생성')
                self.naver =Naver_Posting(self,ID,PW)
                # self.naver = threading.Thread(target=Naver_Posting, args=(self,ID,PW))
                print(type(self.naver))
                # self.naver = threading.Thread(target=Naver_Posting(self,ID,PW))
                self.set_category()


            rows = self.tableWidget.rowCount()

            item_list = []
            checked_rows = []
            for row in range(rows):
                # check if a row is checked 
                checkbox =self.tableWidget.cellWidget(row,0).isChecked()
                if checkbox == True:
                    checked_rows.append(row)


            print(checkbox)
            print(checked_rows)

            # 시간 설정 예외 처리
            if checked_rows != []:
                try:
                    interval = int(self.lineEdit_2.text())
                    # 반복작업체크                    
                    if self.checkBox_9.isChecked():
                        try:
                            total_interval = int(self.lineEdit_5.text())
                        except:
                            QMessageBox.information(self,'Alert!','반복작업을 체크하셨습니다. 전체 대기 시간을 설정해주세요.')
                            raise Exception('again')

                    for row in checked_rows:
                        option_data = self.check_option()
                        row_data = self.get_all_rowitems(row)
                        item_list.append(row_data)

                    print(item_list)
                    # threading.Thread(target=main,args=(self.naver,total_interval,interval,option_data,item_list)).start()

                    try:
                        threading.Thread(target=main,args=(self.naver,total_interval,interval,option_data,item_list)).start()
                    except:
                        self.naver.driver.close()
                except:
                    QMessageBox.information(self,"작업대기시간을 입력하세요","작업대기시간을 입력하세요")
            else:
                QMessageBox.information(self,"등록할 글을 선택해주세요","등록할 글을 선택해주세요")
            

    def get_all_rowitems(self,row):
        """선택된 행의 모든 데이터 리스트로 리턴  """
        
        cols = self.tableWidget.columnCount()
        items = []

        for col in range(cols): 
            item = self.tableWidget.item(row,col).text()
            items.append(item)

        itemlist = {
            "time":items[0],
            "title":items[1],
            "body":items[2],
            "price":items[3],
            "img":items[4],
            "category":items[5],
            "tag":items[6],
            "category_id":items[9]
            }

        print(itemlist)
        return itemlist
           

    def openimagefile(self):
        """
        대표이미지 파일 설정
        """
        fname = QFileDialog.getOpenFileName(self)
        self.lineEdit_4.setText(fname[0])
        
    
    def add_item(self):
        """
        글 리스트에 한 줄 씩 추가
        """
        itemtable = self.tableWidget
        conn = dbmodel()

        import time
        now = time.localtime()
        c_time =  "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        time = c_time
        category = self.comboBox_2.currentText()
        title = self.lineEdit.text()
        price= self.lineEdit_6.text()
        cafe = self.comboBox.currentText()
        category_id = str(self.comboBox_2.currentIndex())
        tag = self.lineEdit_7.text()
        img = self.lineEdit_4.text()
        body = self.textEdit.toPlainText()
        
        #text -> html 
        htmlbody = text_to_html(body)
 

        if title == '':
            QMessageBox.information(self,'Alert!!','제목은 필수항목입니다.')
        elif body == '':
            QMessageBox.information(self,'Alert!!','내용은 필수항목입니다.')
        elif category_id == '0':
            QMessageBox.information(self,"Alert!!", '게시판을 선택해주세요.')
        elif img == '':
            QMessageBox.information(self,"Alert!", '대표이미지는 필수항목입니다.')
        elif price == '':
            QMessageBox.information(self,'Alert!','판매가는 필수항목입니다.')
        elif price != '':
            try:
                print('숫자로 바꿔볼까')
                int(price)
            except:
                print('안바뀌네//')
                QMessageBox.information(self, "Alert!",'판매가는 숫자로 입력해 주세요')
            else:
                print('등록이 되어야 할텐데')
                itemlist = {
                    "time":time,
                    "category":category,
                    "title":title,
                    "price":price,
                    "cafe":cafe,
                    "tag":tag,
                    "img":img,
                    "body":htmlbody,
                    'category_id':category_id
                    }
            
                conn.add_item(itemlist)
                QMessageBox.information(self,"Congrats!!",'게시글이 등록되었습니다!')
                self.tableWidget.clearContents()
                conn.load_data(self.tableWidget)
                conn.close()
                   

    def del_item(self):
        """
        선택 아이템 삭제 
        """ 
        try:
            itemtable = self.tableWidget
            row = itemtable.currentRow()
            print(row)
            id_ = itemtable.item(row, 8).text()

            print(id_)
            conn = dbmodel()
            conn.delete_item(id_)
            print('deleted')
            conn.load_data(itemtable)
            conn.close()
        except:
            QMessageBox.information(self,"ALERT!!","삭제할 행을 선택해 주세요!")


    def clear_items(self):
        # 전체 내용 삭제 
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("delete from items")
        conn.commit()
        conn.close()
     
    def stop_process(self):
        reply = QMessageBox.question(self, 'question','정말로 모든 작업을 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.naver.driver.close()
            time.sleep(0.5)
            try:
                self.naver.driver.switch_to.alert().dismiss()
            except:
                pass
            try:
                self.naver.driver.switch_to.alert().accept()
            except:
                pass
            self.textBrowser.append('작업종료')
        else:
            QMessageBox.information(self,"작업이 이미 중지 되었습니다.","작업이 이미 중지 되었습니다")


    def set_category(self):
        """
        네이버 카페가서 모든 카테고리 크롤링 후 combobox에 구현 
        """
        categorys = self.naver.get_category()
        self.comboBox_2.clear() 
        for cate in categorys:
            self.comboBox_2.addItem(cate)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    myWindow.naver.driver.close()
    kill_process('chromedriver')

app = QApplication(sys.argv)
myWindow = MyWindow()
myWindow.show()
app.exec_()
# myWindow.naver.driver.close()
# kill_process('chromedriver')

    