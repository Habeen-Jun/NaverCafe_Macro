from win32com.client import GetObject
import subprocess

detect_chrome = 0
detect_chromedriver = 0


WMI = GetObject('winmgmts:')
processes = WMI.InstancesOf('Win32_Process')
print(WMI)

for process in processes:
    process = process.Properties_('Name').Value
    print(process)


    if process == 'chrome.exe' :
        print("---크롬 감지---")
        detect_chrome +=1
    elif process == 'chromedriver.exe':
        print("---크롬 드라이버 감지---")
        detect_chromedriver +=1

if detect_chromedriver>=5:
    print("크롬 드라이버 강제종료합니다.")
    subprocess.Popen('taskkill /f /im chromedriver.exe',stdout=subprocess.PIPE) #확인 필요
elif detect_chrome>=20:
    print("크롬 강제종료합니다.")
    subprocess.Popen('taskkill /f /im chrome.exe',stdout=subprocess.PIPE) #확인 필요