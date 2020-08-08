from selenium import webdriver

PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

chrome = webdriver.Chrome('chromedriver.exe')#,options=chrome_options
chrome.get("http://icanhazip.com/")
chrome.get("http://icanhazip.com/")