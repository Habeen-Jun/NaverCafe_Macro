
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import *
import time 
from dbmodel import dbmodel
import threading
from naverposting import Naver_Posting
from naverposting import terminate_thread


# Qtdesigner로 생성한 ui불러옴 
form_class = uic.loadUiType("macro0704.ui")[0]
        
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.login_OK = False 
        self.setupUi(self)
  
        conn = dbmodel()

        # database 정보로드
        self.tableWidget = conn.load_data(self.tableWidget)

        # tabwidget 메뉴 설정  
        self.tabWidget.setTabText(0,'기본 설정')
        self.tabWidget.setTabText(1,'게시글 등록')

        self.tabWidget_2.setTabText(0,'새 글 등록')
        self.tabWidget_2.setTabText(1,'게시글 목록')

        # checkbox 디폴트 체크
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(True)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(True)
        self.checkBox_6.setChecked(False)
        self.checkBox_7.setChecked(False)

        self.checkBox_9.setChecked(True)

        # 작업 대기시간 디폴트 5
        self.lineEdit_2.setText('5')
        # 전체 대기시간 디폴트 10초 
        self.lineEdit_5.setText('10')

        
        # 게시글 테이블
        self.tableWidget.setHorizontalHeaderLabels(["등록날짜","제목", "내용", "가격","대표이미지","카테고리URL",'태그','id'])
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
                print('대기시간: {}'.format(str(interval)))
                # 반복작업체크                    
                if self.checkBox_9.isChecked():
                    try:
                        total_interval = int(self.lineEdit_5.text())
                    except:
                        QMessageBox.information(self,'Alert!','반복작업을 체크하셨습니다. 전체 대기 시간을 설정해주세요.')
                for row in checked_rows:
                    option_data = self.check_option()
                    row_data = self.get_all_rowitems(row)
                    item_list.append(row_data)
                print(option_data)
                print(item_list)
                try:
                    if total_interval == 0:
                        self.textBrowser.append('한 번 만 작업')
                    self.t = Naver_Posting(self, self.driver, option_data, item_list, interval, total_interval)
                    self.t.start()
                    print('-------------------스레드 시작 --------------------------')
                except:
                    self.naver.driver.close()
                    QMessageBox.information(self,'작업오류','작업오류')
            except:
                QMessageBox.information(self,"작업대기시간을 입력하세요","작업대기시간을 입력하세요")
        else:
            QMessageBox.information(self,"등록할 글을 선택해주세요","등록할 글을 선택해주세요")

    @pyqtSlot(object,str,str)
    def reload_naverposting(self,driver,ID,PW):
        """
        작업 중지 되었을 때 Naver_Posting 객체 리로딩 
        """
        self.driver = driver
        self.naver = Naver_Posting(self, self.driver)

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
        conn = dbmodel()

        import time
        now = time.localtime()
        c_time =  "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        time = c_time
        categoryURL = self.lineEdit_8.text()
        title = self.lineEdit.text()
        price= self.lineEdit_6.text()
        tag = self.lineEdit_7.text()
        img = self.lineEdit_4.text()
        body = self.textEdit.toHtml()
    

        if title == '':
            QMessageBox.information(self,'Alert!!','제목은 필수항목입니다.')
        elif body == '':
            QMessageBox.information(self,'Alert!!','내용은 필수항목입니다.')
        elif categoryURL == '0':
            QMessageBox.information(self,"Alert!!", '게시판을 선택해주세요.')
        elif img == '':
            QMessageBox.information(self,"Alert!", '대표이미지는 필수항목입니다.')
        elif price == '':
            QMessageBox.information(self,'Alert!','판매가는 필수항목입니다.')
        elif price != '':
            try:
                int(price)
            except:
                QMessageBox.information(self, "Alert!",'판매가는 숫자로 입력해 주세요')
            else:
                itemlist = {
                    "time":time,
                    "categoryURL":categoryURL,
                    "title":title,
                    "price":price,
                    "tag":tag,
                    "img":img,
                    "body":body,
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
        checkedrows_list = self.get_checked_rows_number()

        if checkedrows_list != []:
            reply = QMessageBox.question(self, 'question','정말로 선택하신 행을 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                itemtable = self.tableWidget
                checkedrows_list = self.get_checked_rows_number()
                print('checked rows : {}'.format(checkedrows_list))
                delete_id_list  = []

                for cheched_row in checkedrows_list:
                    id_ = itemtable.item(cheched_row, 7).text()
                    delete_id_list.append(id_)

                for delete_id in delete_id_list:
                    conn = dbmodel()
                    conn.delete_item(delete_id)
                    print('deleted')

                conn.load_data(itemtable)
                conn.close()
            QMessageBox.information(self, '','성공적으로 행을 삭제했습니다.')
        else:
            QMessageBox.information(self,"ALERT!!","삭제할 행을 선택해 주세요!")
        
    def get_checked_rows_number(self):
        rows = self.tableWidget.rowCount()
        checked_rows_num = []
        row_num = 0
        for row in range(rows):
            # check if a row is checked 
            checkbox =self.tableWidget.cellWidget(row,0).isChecked() 
            if checkbox == True:
                checked_rows_num.append(row_num)
            row_num += 1
        return checked_rows_num

    def clear_items(self):
        # 전체 내용 삭제
        reply = QMessageBox.question(self, 'question','정말로 모든 행을 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute("delete from items")
            conn.commit()
            conn.close()
            QMessageBox.information(self,'','모든 행이 삭제되었습니다.')
     
    def stop_process(self):
        reply = QMessageBox.question(self, 'question','정말로 모든 작업을 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                while self.t.isAlive():
                    time.sleep(0.1)
                    terminate_thread(self.t)
                    self.t.join()
                self.textBrowser.append('작업종료')
            except:
                QMessageBox.information(self,"작업이 이미 중지 되었습니다.","작업이 이미 중지 되었습니다")

    def set_driver(self, driver):
        self.driver = driver
    
    def set_ID(self,ID):
        self.ID = ID 
        print(f'새로 받은 아이디: {self.ID}')
    
    def set_PW(self,PW):
        self.PW = PW
        print(f'새로 받은 비번: {self.PW}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    