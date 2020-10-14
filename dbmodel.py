import sqlite3 
from PyQt5.QtWidgets import *

class dbmodel:
    def __init__(self):
        self.conn = sqlite3.connect('example.db')

    def close(self):
        self.conn.close()

    def load_data(self, tableWidget):
        # ["등록날짜","제목", "내용", "가격","카테고리",'태그','시간','카페','id']
        try:
            sql = "select time, cafe, title, body, price, img, category, tag, id from items"
            result = self.conn.execute(sql)
            print(result)
            # 테이블 초기화 
            tableWidget.clearContents()
            tableWidget.setRowCount(0)

            for row_num, row_data in enumerate(result):
                tableWidget.insertRow(row_num) # 행 추가 
                for col_num, data in enumerate(row_data):
                    checkbox = QCheckBox()
                    tableWidget.setCellWidget(row_num,0,checkbox)
                    tableWidget.setItem(row_num,col_num,QTableWidgetItem(str(data)))

            return tableWidget
        except:
            self.create_table()
           

        return tableWidget

    def create_table(self):
        self.conn.execute('''CREATE TABLE items
                (id integer primary key autoincrement, time text, title text, body text, price text, img text, category text, tag text, cafe text, category_id text)''')
        self.conn.commit()
    
    def add_item(self,itemlist):

        # itemlist = [time, category, title, price, cafe, tag, img]
        data = itemlist
        print(data)
        self.conn.execute("insert into items (time, title, body, price, img, category, tag, cafe) values(?,?,?,?,?,?,?,?)",\
                (data['time'],data['title'],data['body'],data['price'],data['img'],data['categoryURL'],data['tag'],data['address']))
        self.conn.commit()

    def delete_item(self, id_):
        sql = "delete from items where id = ?"
        self.conn.execute(sql,(id_,))
        self.conn.commit()

    def update_item(self, data):
        self.conn.execute("update items set time = ?, title = ?, body = ?, price = ?, img = ?, category = ?, tag = ?, cafe = ? where id = ?",\
                (data['time'],data['title'],data['body'],data['price'],data['img'],data['category'],data['tag'],data['cafe_address'], data['id']))
        self.conn.commit()



    