import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from naverlogin import NaverLoginWindow
from mainwindow import MyWindow
from login import LoginWindow



class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = LoginWindow()
        self.login.switch_window.connect(self.show_naverlogin)
        self.login.show()
    
    def show_naverlogin(self):
        self.naverlogin = NaverLoginWindow()
        self.login.close()
        self.naverlogin.switch_window.connect(self.show_main)
        self.naverlogin.show()

    def show_main(self):
        self.window = MyWindow()
        self.naverlogin.close()
        self.window.show()

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()