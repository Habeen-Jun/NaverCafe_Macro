from selenium import webdriver
import time
from PyQt5.QtCore import * 
from PyQt5 import QtCore
class Naverlogin(QtCore.QThread):

    # finished = pyqtSignal(object)
    finished = pyqtSignal(object)

    def __init__(self):
        QThread.__init__(self)
        print("worker thread created!")
        
    def run(self,ID,PW):
        
        print('thread running..')

        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
        #options.add_argument("headless")
        self.driver = webdriver.Chrome('chromedriver',options=options)
        url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
        # 네이버 로그인 url 접속
        self.driver.get(url)
        # 캡챠(봇 감지) 우회를 위해 execute_script 함수로 id, pw 입력
        self.driver.execute_script("document.getElementsByName('id')[0].value='" + ID + "'")
        time.sleep(0.5)
        self.driver.execute_script("document.getElementsByName('pw')[0].value='" + PW + "'")
        time.sleep(0.5)
        # 로그인 버튼을 찾아 클릭
        self.driver.find_element_by_xpath('//*[@id="log.login"]').click()
        print('login success')
        
        self.finished.emit(self.driver)

    # def run(self):
    #     print('thread runnning')
    #     self.login()
        # self.finished.emit(self.driver)
if __name__ =='__main__':
    t = Naverlogin('junhabeen', 'wjsgkqls123')
    t.start()
    