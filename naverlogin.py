from selenium import webdriver
import time
from PyQt5.QtCore import * 
from PyQt5 import QtCore
class Naverlogin(QtCore.QThread):
    # 로그인 작업이 끝나면 driver, ID, PW 를 반환 
    finished = pyqtSignal(object,str,str)

    def __init__(self):
        QThread.__init__(self)
        print("worker thread created!")
        
    def run(self):
        
        print('thread running..')
        self.ID
        self.PW 

        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
        #options.add_argument("headless")
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
        print('login success')
        self.finished.emit(self.driver,self.ID, self.PW)
        print('emited')

    def set_ID(self,ID):
        self.ID = ID
    def set_PW(self,PW):
        self.PW = PW

