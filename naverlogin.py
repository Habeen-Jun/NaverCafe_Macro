from selenium import webdriver
import time
from PyQt5.QtCore import * 
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from selenium_python import get_driver_settings, smartproxy
# from fake_useragent import UserAgent
class Naverlogin(QtCore.QThread):
    # 로그인 작업이 끝나면 driver, ID, PW 를 반환 
    finished = pyqtSignal(object,str,str,bool)

    def __init__(self):
        QThread.__init__(self)
        print("worker thread created!")
        
    def run(self):
        
        print('thread running..')
        self.ID
        self.PW 
        ua = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument(str(ua.random))
        #options.add_argument("headless")
        print(smartproxy())
        self.driver = webdriver.Chrome('chromedriver',options=options)
        url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
        # 네이버 로그인 url 접속
        self.driver.get(url)
        # 캡챠(봇 감지) 우회를 위해 execute_script 함수로 id, pw 입력
        self.driver.execute_script("document.getElementsByName('id')[0].value='" + self.ID + "'")
        time.sleep(0.5)
        self.driver.execute_script("document.getElementsByName('pw')[0].value='" + self.PW + "'")
        time.sleep(0.5)
        # 로그인 버튼을 찾아 클릭
        self.driver.find_element_by_xpath('//*[@id="log.login"]').click()
       
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="err_common"]')
            login_ok = False
            print('로그인 실패')
        except:
            login_ok = True 

        self.finished.emit(self.driver,self.ID, self.PW, login_ok)
         

    def set_ID(self,ID):
        self.ID = ID
    def set_PW(self,PW):
        self.PW = PW

