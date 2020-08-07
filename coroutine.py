import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
import pymysql
from datetime import datetime
class LoginForm(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Login Form')
		self.resize(500, 120)

		layout = QGridLayout()

		label_name = QLabel('<font size="4"> 아이디 </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('ID')
		layout.addWidget(label_name, 0, 0)
		layout.addWidget(self.lineEdit_username, 0, 1)

		label_password = QLabel('<font size="4"> 비밀번호 </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('password')
		layout.addWidget(label_password, 1, 0)
		layout.addWidget(self.lineEdit_password, 1, 1)

		button_login = QPushButton('Login')
		button_login.clicked.connect(self.check_password)
		layout.addWidget(button_login, 2, 0, 1, 2)
		layout.setRowMinimumHeight(2, 75)

		self.setLayout(layout)

	def check_password(self):

            ID = self.lineEdit_username.text()
            PW = self.lineEdit_password.text()

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


if __name__ == '__main__':
	app = QApplication(sys.argv)

	form = LoginForm()
	form.show()

	sys.exit(app.exec_())

 