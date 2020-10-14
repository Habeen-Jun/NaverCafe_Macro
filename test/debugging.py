from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions  import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pyautogui 
import time


options = Options()
options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
webdriver.ChromeOptions()
driver = webdriver.Chrome(r'C:\Users\PC\Documents\GitHub\NaverCafe_Macro\chromedriver.exe',options=options)
# driver.get('https://cafe.naver.com/4uloveme?iframe_url=%2FArticleWrite.nhn%3Fclubid%3D23465858%26m%3Dwrite')
wait = WebDriverWait(driver, 3)
driver.switch_to_frame('cafe_main')
comments_not_allow  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/div/ul/li[2]/a')))
driver.execute_script('arguments[0].click();',comments_not_allow)
# comments_not_allow.click()
# '/html/body/div[3]/div/div/div/div/ul/li[2]/a'
cafe_share_not_allow  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div/div/div/ul/li[2]/a')))
driver.execute_script('arguments[0].click();',cafe_share_not_allow)

share_not_allow  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[9]/div/div/div/div/ul/li[2]/a')))
driver.execute_script('arguments[0].click();',share_not_allow)
 
right_click_not_allow  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/div/div/div/div/ul/li[2]/a')))
driver.execute_script('arguments[0].click();',right_click_not_allow)

 
not_to_all  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/form[1]/div[1]/div[1]/div/ul[2]/li[3]/div[1]/input[2]')))
driver.execute_script('arguments[0].click();',not_to_all)

'/html/body/div[6]/div/div/div/div/ul/li[1]/a'
use_CCL  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[6]/div/div/div/div/ul/li[1]/a')))
driver.execute_script('arguments[0].click();',use_CCL)