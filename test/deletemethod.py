from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions  import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pyautogui 
import time
from bs4 import BeautifulSoup

options = Options()
options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
webdriver.ChromeOptions()
driver = webdriver.Chrome(r'C:\Users\PC\Documents\GitHub\NaverCafe_Macro\chromedriver.exe',options=options)

def del_samepost(self,title):
    wait = WebDriverWait(driver, 3)
    driver.get('https://cafe.naver.com/4uloveme')
    user_profile = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="cafe-info-data"]/ul/li[3]/p/a')))
    user_profile.click()
    my_posts = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ia-action-data"]/div[2]/ul/li[2]/span/strong/a')))
    my_posts.click()
    driver.switch_to_frame('cafe_main')
    driver.switch_to_frame('innerNetwork')

    soup = BeautifulSoup(driver.page_source,'html.parser')
    rows = soup.find_all('tr')
    
    title = 'S급'
    item_list = []
    cnt = 1
    for row in rows:
        try:
            row = row.find('a').text.strip()
            item_list.append(row)
        except:
            pass
    for item in item_list:
        if title in item:
            print(item)
            print(cnt)
            break
        else:
            cnt += 1

    post_to_delete = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-area"]/div[1]/table/tbody/tr['+str(cnt)+']/td[1]/div[1]')))
    post_to_delete.click()
    delete_button = wait.until(EC.presence_of_element_located((By.ID,'a_remove')))
    delete_button.click()
    driver.switch_to_alert().accept()