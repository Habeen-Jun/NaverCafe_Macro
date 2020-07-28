import threading 
import time
from bs4 import BeautifulSoup
import ctypes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions  import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
# finally successed..
def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    print(thread)
    if not thread.isAlive():
        return
    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

#################################

#예외 발생으로 종료 성공 

##################################
class Naver_Posting(threading.Thread):
    def __init__(self, window, driver, option_data, item_list, interval):
        threading.Thread.__init__(self)
        self.window = window
        self.driver = driver
        self.option_data = option_data
        self.item_list = item_list
        self.interval = interval

    def set_option_data(self,option_data):
        self.option_data = option_data
    def set_item_list(self, item_list):
        self.item_list = item_list
    def set_interval(self, interval):
        self.interval =  interval
        
    def run(self):
        interval = self.interval
        option_data = self.option_data
        item_list = self.item_list
        try:
            while True:
                print('do the thing')
                self.window.textBrowser.append("총 {} 개 게시글을 등록합니다.".format(str(len(item_list))))
                print("총 {} 개 게시글을 등록합니다.".format(str(len(item_list))))
                for item in item_list:

                    self.window.textBrowser.append('작업대기시간: {}'.format(str(interval)))
                    print(item)
                

                    driver = self.driver
                    print(driver)
                    
                    driver.get(item['category'])

                    # wait for iframe to be loaded 
                    wait = WebDriverWait(driver,20)
                    wait.until(EC.presence_of_element_located((By.ID,'cafe_main')))
                    
                    driver.switch_to_frame('cafe_main')

                    # '글쓰기' 발견할 때까지 기다림
                    # 20초까지 기다림 
                    wait = WebDriverWait(driver,20)
                    buttons = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="writeFormBtn"]')))
                    buttons.click()

                    self.Selling_Post_Process(option_data, item)
                    # try:
                    #     alert = driver.switch_to_alert()
                    #     alert.accept()
                    # except: 
                    #     pass
                    # print('카페접속')

                    # try:
                    #     driver.find_element_by_xpath('//*[@id="seOneArticleFormBannerCloseBtn"]').click()
                    #     print('배너 창 닫음')
                    # except:
                    #     pass
                    

                    # time.sleep(2)

                    # # 카페 글등록 클릭
                    # sample = driver.find_element_by_xpath('//*[@id="cafe-info-data"]/div[2]/a')
                    # driver.execute_script("arguments[0].click();", sample)
                    # driver.implicitly_wait(3)
                    # print('카페 글등록 클릭.')

                    # # 카페 메인 프레임 진입 
                    # driver.switch_to.frame("cafe_main")

                    # # 카테고리 선택
                    # time.sleep(1)
                    # driver.find_element_by_xpath('//*[@id="boardCategory"]').click()
                    # category_num = str(int(item['category_id'])+1)
                    # driver.find_element_by_xpath('//*[@id="boardCategory"]/option['+category_num+']').click()
                    # time.sleep(2)


                    # try:
                    #     alert = driver.switch_to_alert()
                    #     alert.accept()
                    #     # 경고메세지가 뜬 건 판매글임
                    #     print('alert accepted')
                    #     selling_post = 1
                    # except:
                    #     selling_post = 0
                    
                    # if selling_post == 1:
                    #     self.window.textBrowser.append('판매글 게시판')
                    #     self.Selling_Post_Process(option_data, item)
                    # else:
                    #     print('no alert')
                    #     self.window.textBrowser.append('일반 게시판')
                    #     self.Post_Process(option_data,item)

                    # # 각 게시물 간 interval
                    # time.sleep(int(interval))
        finally:
            self.window.textBrowser.append('--------------------------------------')
            self.window.textBrowser.append('작업이 중지 되었거나 네트워크 문제가 발생했습니다.')
            print('ended')

    def Selling_Post_Process(self,option_data,item):
        """
        판매글 게시판 프로세스
        :param: option_data, item
        """
        driver = self.driver
        try:
            # # 20초까지 기다림 
            # wait = WebDriverWait(driver,20)
            # # '나중에 하기' 발견할 때까지 기다림
            # buttons = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '나중에 하기')]")))
            # buttons.click()
            driver.find_element_by_xpath('//*[@id="main-area"]/div[3]/div[1]/div/a[2]/img').click()
            driver.find_element_by_xpath('//*[@id="subject"]').click()
        except:
            pass
       
        time.sleep(2)

        # 대표이미지 삽입
        # 새 창이 로드 되면 TRUE 를 리턴하는 함수
        def found_window():
            def predicate(driver):
                try:
                    img_win = driver.window_handles[1]
                    driver.switch_to_window(img_win)
                except IndexError:
                    return False
                else:
                    return True # found window
            return predicate
        
        
        # 클릭 했을 때 오류가 뜨지 않았는데 .. 왜 창은 안뜰까?
        wait = WebDriverWait(driver,20)
        buttons = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="iImage"]/a/strong')))
        buttons.click()
        # driver.find_element_by_xpath('//*[@id="iImage"]/a/strong').click()
        # 50 초까지 기다림. 
        WebDriverWait(driver, timeout=50).until(found_window())
        img_win = driver.window_handles[1]
        original_win =driver.window_handles[0]
        driver.switch_to_window(img_win)

        print(driver.window_handles)

        

        soup = BeautifulSoup(driver.page_source,'html.parser')

        if soup.find('strong',{'class':'tit'}) != None:
                try:
                    driver.find_element_by_xpath('//*[@id="footer"]/a').click()
                    print('매니져위임창 닫음')
                except:
                    print('매니져위임창 못 닫음')

        try:
            driver.switch_to_window(driver.window_handles[1])
            driver.find_element_by_xpath('/html/body/div[2]/div/button').click()
        except:
            print('창안닫침')

        
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="pc_image_file"]').send_keys(item['img'])
        self.window.textBrowser.append('대표 이미지 삽입 완료')
        # 20초까지 기다림 
        wait = WebDriverWait(driver,20)
        # '올리기' 발견할 때까지 기다림
        buttons = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '올리기')]")))
        buttons.click()

        driver.switch_to_window(original_win)
        driver.switch_to_frame('cafe_main')


        # option_data 처리 

        if option_data['phone_show'] == True:
            driver.find_element_by_xpath('//*[@id="sale_open_phone"]').click()
            if option_data['use_disposable'] == True:
                driver.find_element_by_xpath('//*[@id="sale_otn_use"]').click()
            

        if option_data['allow_comments'] == True:
            pass
        else:
            driver.find_element_by_xpath('//*[@id="replyynspan"]').click()
            try:
                time.sleep(1)
                driver.switch_to_alert().accept()
                self.window.textBrowser.append('매니저가 댓글설정을 허용하지 않았습니다.')
                print('alert accepted')
            except:
                driver.find_element_by_xpath('//*[@id="layerReplyYnSpan"]/div/div/div/div/ul/li[2]/a').click()


        if option_data['alarm_to_all'] == True:
            driver.find_element_by_xpath('//*[@id="all_open"]').click()
        else:
            driver.find_element_by_xpath('//*[@id="member_open"]').click()
        
        if option_data['searched'] == True:
            driver.find_element_by_xpath('//*[@id="search_conform"]').click()
        
        if option_data['allow_rightclick'] == True:
            pass
        else:
            driver.find_element_by_xpath('//*[@id="rclickspan"]').click()
            try:
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="layerRclickYnSpan"]/div/div/div/div/ul/li[2]').click()
            except:
                print('click unabled')
                pass
        

        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 제목 삽입
        time.sleep(1)
        driver.execute_script("document.getElementsByName('subject')[0].value='" + item['title'] + "'")
        self.window.textBrowser.append('제목 입력 완료')
        # 가격 
        try:
            driver.find_element_by_xpath('//*[@id="sale_cost"]').send_keys(item['price'])
            self.window.textBrowser.append('가격 입력 완료')
        except:
            pass

        print('제목넣음')

        iframe = soup.find_all('iframe')

        # 글쓰는 칸 진입
        driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])


        ##########################################
        #여기서부터 html 소스 작업코드
        ##########################################

        # text insert with execute_script()
        node = driver.find_element_by_xpath("/html/body")
        script = """arguments[0].insertAdjacentHTML('afterbegin', arguments[1])"""
        driver.execute_script(script, node, item['body'])
        self.window.textBrowser.append('본문 내용 입력 완료')

        driver.switch_to.default_content()
        driver.switch_to.frame("cafe_main")

        driver.find_element_by_xpath('//*[@id="cafewritebtn"]/strong').click()
        self.window.textBrowser.append('글등록완료')
        print('글등록완료')
        time.sleep(2)

        print('열린 탭:{}'.format(driver.window_handles))
            
    def Post_Process(self,option_data, item):
        """
        일반글 게시판 프로세스
        :param: option_data, item
        """
        driver = self.driver
        # 제목 삽입
        self.window.textBrowser.append('일반글 게시판')
        time.sleep(1)
        driver.execute_script("document.getElementsByName('subject')[0].value='" + item['title'] + "'")
        self.window.textBrowser.append('제목입력완료')
        # 가격 
        try:
            driver.find_element_by_xpath('//*[@id="sale_cost"]').send_keys(item['price'])
            self.window.textBrowser.append('가격입력완료')
        except:
            pass

        soup = BeautifulSoup(driver.page_source,'html.parser')

        iframe = soup.find_all('iframe')

        # 글쓰는 칸 진입
        driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])


        ##########################################
        #여기서부터 html 소스 작업코드
        ##########################################

        # text insert with execute_script()
        node = driver.find_element_by_xpath("/html/body") 
        # script = """arguments[0].insertAdjacentHTML('afterbegin',  "<h1>" + arguments[1] + "</h1>")"""
        script = """arguments[0].insertAdjacentHTML('afterbegin', arguments[1])"""
        driver.execute_script(script, node, item['body'])
        self.window.textBrowser.append('본문내용 입력완료')

        driver.switch_to.default_content()
        driver.switch_to.frame("cafe_main")


        if option_data['allow_comments'] == True:
            pass
        else:
            driver.find_element_by_xpath('//*[@id="replyynspan"]').click()
            try:
                time.sleep(1)
                driver.switch_to_alert().accept()
                self.window.textBrowser.append('매니저가 댓글설정을 허용하지 않았습니다.')
                print('alert accepted')
            except:
                driver.find_element_by_xpath('//*[@id="layerReplyYnSpan"]/div/div/div/div/ul/li[2]/a').click()


        if option_data['alarm_to_all'] == True:
            driver.find_element_by_xpath('//*[@id="all_open"]').click()
        else:
            driver.find_element_by_xpath('//*[@id="member_open"]').click()
        
        if option_data['searched'] == True:
            driver.find_element_by_xpath('//*[@id="search_conform"]').click()
        
        if option_data['allow_rightclick'] == True:
            pass
        else:
            driver.find_element_by_xpath('//*[@id="rclickspan"]').click()
            driver.find_element_by_xpath('//*[@id="layerRclickYnSpan"]/div/div/div/div/ul/li[2]/a').click()


        driver.find_element_by_xpath('//*[@id="cafewritebtn"]/strong').click()
        print('글등록완료')
        self.window.textBrowser.append('글등록 완료')
        time.sleep(2)

        print('열린 탭:{}'.format(driver.window_handles))

class Cafe_Menu_Getter:
    def __init__(self, driver):
        self.driver = driver 

    def get_category(self, cafe_name):

        cafes = {
            '중고나라':'joonggonara',
            '중고폰나라':'4uloveme.cafe',
        }

        driver = self.driver

        cafe_baseurl = 'https://cafe.naver.com/'
        cafe_plusurl = cafes[cafe_name]

        driver.get(cafe_baseurl+cafe_plusurl)

        try:
            driver.find_element_by_xpath('//*[@id="seOneArticleFormBannerCloseBtn"]').click()
        except:
            pass

        # 카페 글등록 클릭 
        try:
            sample = driver.find_element_by_xpath('//*[@id="cafe-info-data"]/div[2]/a')
            driver.execute_script("arguments[0].click();", sample)
            driver.implicitly_wait(3)
        except:
            sample = driver.find_element_by_xpath('//*[@id="cafe-info-data"]/div[3]/a ')
            driver.execute_script("arguments[0].click();", sample)
            driver.implicitly_wait(3)


        # 카페 메인 프레임 진입 
        driver.switch_to.frame("cafe_main")
        time.sleep(1)
        print('cafe main')
        soup = BeautifulSoup(driver.page_source,'html.parser')
        time.sleep(1)
        menus = soup.find('select',{'name':'menuid'})
        # print(menus)
        category = []
        menus = menus.find_all('option')
            
        for menu in menus:
            cate = menu.text
            category.append(cate)
        
        return category

