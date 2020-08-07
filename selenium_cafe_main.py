from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions  import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pyautogui
import re 

options = webdriver.ChromeOptions()

driver = webdriver.Chrome('chromedriver.exe',options=options)
url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'

driver.get(url)
# 캡챠(봇 감지) 우회를 위해 execute_script 함수로 id, pw 입력
driver.execute_script("document.getElementsByName('id')[0].value='" + 'junhabeen' + "'")
time.sleep(0.5)
driver.execute_script("document.getElementsByName('pw')[0].value='" + 'wjsgkqls123' + "'")
time.sleep(0.5)
# 로그인 버튼을 찾아 클릭
driver.find_element_by_xpath('//*[@id="log.login"]').click()
print('login success')

def convert_url(url):
    menuidmatch = re.search('menuid=\d{4}',url)
    clubidmatch = re.search('clubid=\d{8}', url)
    menuid = menuidmatch[0].split('=')[1]
    clubid = clubidmatch[0].split('=')[1]
    return 'https://cafe.naver.com/ca-fe/cafes/'+clubidmatch+'/menus/'+menuidmatch+'/articles/write?boardType=L'

 
url = ''
re.compile('menuid=\d{4}')
# driver.get('https://cafe.naver.com/ca-fe/cafes/10050146/articles/write?boardType=L')
driver.get('https://cafe.naver.com/ca-fe/cafes/10050146/articles/write?boardType=L')
driver.get('https://cafe.naver.com/ca-fe/cafes/10050146/menus/1731/articles/write?boardType=L')

time.sleep(3)
 
soup = BeautifulSoup(driver.page_source, 'html.parser')

# driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[3]/div[7]/div/div/div[3]/a[2]/span')
try:
    wait = WebDriverWait(driver,20)
    auth_close_button = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '미인증 상태로 글쓰기')]")))
    auth_close_button.click()
    print('미인증 사용지')
except:
    print('인증 사용자')

driver.switch_to_alert().accept()

# title 
driver.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[1]/div[2]/div/textarea').send_keys('title')
# price
price_input = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/input')))
price_input.send_keys('10000')


# 상품상태
# 미개봉 = quality1 거의 새것 = quality2 사용감있음 = quality3

quality = 'quality1'
button = wait.until(EC.presence_of_element_located((By.ID,quality)))
driver.execute_script("arguments[0].click();",button)


# 배송방법
# 직거래 = delivery0 택배거래 = delivery1 온라인전송 = delivery2
button = wait.until(EC.presence_of_element_located((By.ID,'delivery0')))
driver.execute_script("arguments[0].click();",button)


# 사진 업로드 
# wait = WebDriverWait(driver,20)
# photo_upload_button = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="SmartEditor"]/div/div[1]/div/header/div[1]/ul/li[1]/button')))
# driver.execute_script("arguments[0].click();",photo_upload_button)
# time.sleep(3)
# pyautogui.write(r"C:\Users\PC\Pictures\캡처.png")
# time.sleep(30)
# pyautogui.press('enter')
print('사진 입력')


# body
driver.find_element_by_xpath('//*[@id="SmartEditor"]/div/div[1]/div/div[1]/div[2]/section').click()
pyautogui.write('안녕하세요')
# elem = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/section/article/div/div/div/div/div/p/span[1]')))
# elem.send_keys('10000')
# elem.send_keys('helloo')
# script = """arguments[0].insertAdjacentHTML('afterbegin', arguments[1])"""
# driver.execute_script(script, elem, '안녕하세요')


button = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '카페 공유 허용')]")))
driver.execute_script('arguments[0].click();',button)
button = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '외부 공유 허용')]")))
driver.execute_script('arguments[0].click();',button)
button = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '저장 허용')]")))
driver.execute_script('arguments[0].click();',button)
button = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '자동출처 사용')]")))
driver.execute_script('arguments[0].click();',button)

# 글등록
post_button = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div/a/span')))
driver.execute_script('arguments[0].click();',post_button)