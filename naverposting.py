import threading 
import time
from bs4 import BeautifulSoup
import ctypes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions  import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re 
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
    def __init__(self, window, driver, option_data, item_list, interval, total_interval):
        threading.Thread.__init__(self)
        self.window = window
        self.driver = driver
        self.option_data = option_data
        self.item_list = item_list
        self.interval = interval
        self.total_interval = total_interval

    def set_option_data(self,option_data):
        self.option_data = option_data
    def set_item_list(self, item_list):
        self.item_list = item_list
    def set_interval(self, interval):
        self.interval =  interval

    def convert_url(self,url):
        menuidmatch = re.search('menuid=\d{4}',url)
        clubidmatch = re.search('clubid=\d{8}', url)
        menuid = menuidmatch[0].split('=')[1]
        clubid = clubidmatch[0].split('=')[1]
        return 'https://cafe.naver.com/ca-fe/cafes/'+clubidmatch+'/menus/'+menuidmatch+'/articles/write?boardType=L'
    
    def run(self):
        if self.option_data['keep_update'] == True:
            self.post_repeat()
        else:
            print('한 번만 등록')
            self.post_once()
    def post_once(self):
        interval = self.interval
        option_data = self.option_data
        item_list = self.item_list
        try:
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append("[{}] 총 {} 개 게시글을 한 번만 등록합니다.".format( c_time, str(len(item_list))) )
            print("[{}] 총 {} 개 게시글을 등록합니다.".format(c_time, str(len(item_list))))
            for item in item_list:
                c_time = self.getFormattedCurrentTime()
                print(item)

                if option_data['delete_post']:
                    self.del_samepost(item['title'])
            

                driver = self.driver
                # url = self.convert_url(item['category'])
                url = item['address']+'?iframe_url=%2FArticleWrite.nhn%3Fclubid%3D23465858%26m%3Dwrite'
                # url = 'https://cafe.naver.com/4uloveme?iframe_url=%2FArticleWrite.nhn%3Fclubid%3D23465858%26m%3Dwrite'
                
                # Nosuchwindowexception 발생 시 예외 처리
                try:
                    driver.get(url)
                except NoSuchWindowException:
                    original_win = driver.window_handles[0]
                    driver.switch_to_window(original_win)
                    driver.get(url)

                # 오류 발생 후 작업 재시작시 Alert 창 handle 
                try:
                    wait = WebDriverWait(driver,2)
                    alert = wait.until(EC.alert_is_present(),'Timed out waiting for PA creation ' +
                                'confirmation popup to appear.')
                    alert = driver.switch_to.alert
                    alert.accept() 
                except TimeoutException:
                    print('no alert')

                # wait for iframe to be loaded 
                wait = WebDriverWait(driver,20)
                wait.until(EC.presence_of_element_located((By.ID,'cafe_main')))
                driver.switch_to_frame('cafe_main')
                
                wait = WebDriverWait(driver,3)

                # 메뉴 선택 
                # menu_detail = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '"+item['category']+"')]")))
                menu_detail = wait.until(EC.presence_of_element_located((By.XPATH,"//option[text()='"+item['category']+"']")))
                menu_detail.click()
                # driver.execute_script("arguments[0].click();", menu_detail)

                try:
                    alert = wait.until(EC.alert_is_present(),'Timed out waiting for PA creation ' +
                                'confirmation popup to appear.')
                    alert = driver.switch_to.alert
                    alert.accept()
                    selling_post = 1 
                except TimeoutException:
                    print('no alert')
                    selling_post = 0 

                if selling_post == 1:
                    self.Selling_Post_Process(option_data, item)
                else: 
                    self.Post_Process(option_data, item)

                # 각 게시물 간 interval
                # 마지막 게시물은 대기하지 않고 건너뛰기.

                c_time = self.getFormattedCurrentTime()
                self.window.textBrowser.append('[{}] 게시글 간 대기 시간: {}'.format(c_time,str(interval)))
                if len(item_list) > 1 and item != item_list[-1]:
                    interval = int(interval)
                    print('[게시물간대기]'+str(interval)+'초 대기')
                    for i in range(interval):
                        time.sleep(1)
                        # print('[게시물간대기]'+str(i)+'초기다림.')
                else:
                    pass

                self.window.textBrowser.append('--------------------------------------')

        finally:
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append('--------------------------------------')
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append('[{}] 사용자가 작업을 중지 했거나 네트워크 문제가 발생했습니다.'.format(c_time))
            # print('ended')

    def post_repeat(self):
        interval = self.interval
        option_data = self.option_data
        item_list = self.item_list
        try:
            while True:
                c_time = self.getFormattedCurrentTime()
                self.window.textBrowser.append("[{}] 총 {} 개 게시글을 반복적으로 등록합니다.".format( c_time, str(len(item_list))) )
                print("[{}] 총 {} 개 게시글을 등록합니다.".format(c_time, str(len(item_list))))
                for item in item_list:
                    c_time = self.getFormattedCurrentTime()
                    print(item)

                    if option_data['delete_post']:
                        self.del_samepost(item['title'],item['address'])
                

                    driver = self.driver
                    # url = 'https://cafe.naver.com/4uloveme?iframe_url=%2FArticleWrite.nhn%3Fclubid%3D23465858%26m%3Dwrite'
                    url = item['address']+'?iframe_url=%2FArticleWrite.nhn%3Fclubid%3D23465858%26m%3Dwrite'
                    
                    # Nosuchwindowexception 발생 시 예외 처리
                    try:
                        driver.get(url)
                    except NoSuchWindowException:
                        original_win = driver.window_handles[0]
                        driver.switch_to_window(original_win)
                        driver.get(url)

                    # 오류 발생 후 작업 재시작시 Alert 창 handle 
                    try:
                        wait = WebDriverWait(driver,2)
                        alert = wait.until(EC.alert_is_present(),'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')
                        alert = driver.switch_to.alert
                        alert.accept() 
                    except TimeoutException:
                        print('no alert')

                    # wait for iframe to be loaded 
                    wait = WebDriverWait(driver,20)
                    wait.until(EC.presence_of_element_located((By.ID,'cafe_main')))
                    driver.switch_to_frame('cafe_main')
                    
                    wait = WebDriverWait(driver,3)

                    # 메뉴 선택 
                    # menu_detail = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '"+item['category']+"')]")))
                    menu_detail = wait.until(EC.presence_of_element_located((By.XPATH,"//option[text()='"+item['category']+"']")))
                    menu_detail.click()
                    # driver.execute_script("arguments[0].click();", menu_detail)

                    try:
                        alert = wait.until(EC.alert_is_present(),'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')
                        alert = driver.switch_to.alert
                        alert.accept()
                        selling_post = 1 
                    except TimeoutException:
                        print('no alert')
                        selling_post = 0 

                    if selling_post == 1:
                        self.Selling_Post_Process(option_data, item)
                    else: 
                        self.Post_Process(option_data, item)

                    self.window.textBrowser.append('--------------------------------------')

                    # 각 게시물 간 interval
                    if len(item_list) > 1 and item != item_list[-1]:
                        interval = int(interval)
                        c_time = self.getFormattedCurrentTime()
                        self.window.textBrowser.append('[{}] 게시글 간 대기 시간: {}'.format(c_time,str(interval)))
                        print('[게시물간대기]'+str(interval)+'초 대기')
                        for i in range(interval):
                            time.sleep(1)
                            print('[게시물간대기]'+str(i)+'초기다림.')
                    else:
                        pass
                total_interval = int(self.total_interval)
                c_time = self.getFormattedCurrentTime()
                self.window.textBrowser.append('[{}] 전체 대기 시간: {}'.format(c_time,str(total_interval)))
                print('[전체대기]'+str(total_interval)+'초기다림')
                for i in range(total_interval):
                    time.sleep(1)
                    print('[전체대기]'+str(i)+'초기다림.')
        finally:
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append('--------------------------------------')
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append('[{}] 사용자가 작업을 중지 했거나 네트워크 문제가 발생했습니다.'.format(c_time))
            # print('ended')

    def Selling_Post_Process(self,option_data,item):
        """
        판매글 게시판 프로세스
        :param: option_data, item
        """
        driver = self.driver
        try:
            driver.find_element_by_xpath('//*[@id="main-area"]/div[3]/div[1]/div/a[2]/img').click()
            driver.find_element_by_xpath('//*[@id="subject"]').click()
        except:
            pass
       
        time.sleep(2)

        # 대표이미지 삽입
        self.upload_photo_process(item)

        original_win =driver.window_handles[0]
        driver.switch_to_window(original_win)
        driver.switch_to_frame('cafe_main')

        # 제목 삽입
        time.sleep(1)
        # /n 들어갔을 때 javascript 에러 뜸 
        driver.execute_script("document.getElementsByName('subject')[0].value='" + item['title'] + "'")
        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 제목 입력 완료'.format(c_time))
        # 가격 
        try:
            driver.find_element_by_xpath('//*[@id="sale_cost"]').send_keys(item['price'])
            self.window.textBrowser.append('[{}] 가격 입력 완료'.format(c_time))
        except:
            pass
        



        # option_data 처리
        wait = WebDriverWait(driver,3)
        if option_data['naver_pay'] == False:
            direct_pay = wait.until(EC.presence_of_element_located((By.ID,'sale_direct')))
            direct_pay.click()
        else: 
            # naver_pay 
            wait = WebDriverWait(driver,3)
            npay_buttons = wait.until(EC.presence_of_element_located((By.ID,"pay_corp_N")))
            npay_buttons.click()

            agree = wait.until(EC.presence_of_element_located((By.ID,"sale_chk_agree")))
            agree.click()

        if option_data['allow_cafe_share'] == False:
            cafe_share_not_allow  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div/div/div/ul/li[2]/a')))
            driver.execute_script('arguments[0].click();',cafe_share_not_allow)

        if option_data['phone_show'] == True:
            driver.find_element_by_xpath('//*[@id="sale_open_phone"]').click()
            if option_data['use_disposable'] == True:
                driver.find_element_by_xpath('//*[@id="sale_otn_use"]').click()
        
        # 댓글허용 미 체크 시
        if option_data['allow_comments'] == False:
            comments_not_allow  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/div/ul/li[2]/a')))
            driver.execute_script('arguments[0].click();',comments_not_allow)
       
        if option_data['alarm_to_all'] == False:
            not_to_all  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/form[1]/div[1]/div[1]/div/ul[2]/li[3]/div[1]/input[2]')))
            driver.execute_script('arguments[0].click();',not_to_all)

        if option_data['CCL'] == True:
            use_CCL  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[6]/div/div/div/div/ul/li[1]/a')))
            driver.execute_script('arguments[0].click();',use_CCL)
        
        if option_data['allow_rightclick'] == False:
            right_click_not_allow  = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/div/div/div/div/ul/li[2]/a')))
            driver.execute_script('arguments[0].click();',right_click_not_allow)
 
 
        

        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 태그 입력 
        wait = WebDriverWait(driver,3)
        tag_input = wait.until(EC.presence_of_element_located((By.ID,'tagnames')))
        tag_input.click()
        tag_input.send_keys(item['tag'])

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
        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 본문 내용 입력 완료'.format(c_time))

        driver.switch_to.default_content()
        driver.switch_to.frame("cafe_main")

        driver.find_element_by_xpath('//*[@id="cafewritebtn"]/strong').click()


        try:
            wait = WebDriverWait(driver,3)
            alert = wait.until(EC.alert_is_present(),'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')
            alert = driver.switch_to.alert
            msg = alert.text
            alert.accept() 
            if 'JPG' in msg:
                self.upload_photo_process(item)
                print('사진다시')
        except TimeoutException:
            pass 

        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 글등록완료'.format(c_time))
        print('글등록완료')
        

        print('열린 탭:{}'.format(driver.window_handles))
            
    def Post_Process(self,option_data, item):
        """
        일반글 게시판 프로세스
        :param: option_data, item
        """
        driver = self.driver
        # 제목 삽입
        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 일반글 게시판'.format(c_time))
        time.sleep(1)
        self.window.textBrowser.append('[{}] 등록할 글: {}'.format(c_time, item['title']))
        driver.execute_script("document.getElementsByName('subject')[0].value='" + item['title'] + "'")
        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 제목입력완료'.format(c_time))
        # 가격 
        try:
            driver.find_element_by_xpath('//*[@id="sale_cost"]').send_keys(item['price'])
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append('[{}] 가격입력완료'.format(c_time))
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
        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 본문내용 입력완료'.format(c_time))

        driver.switch_to.default_content()
        driver.switch_to.frame("cafe_main")


        if option_data['allow_comments'] == True:
            pass
        else:
            driver.find_element_by_xpath('//*[@id="replyynspan"]').click()
            try:
                time.sleep(1)
                driver.switch_to_alert().accept()
                c_time = self.getFormattedCurrentTime()
                self.window.textBrowser.append('[{}] 매니저가 댓글설정을 허용하지 않았습니다.'.format(c_time))
                print('alert accepted')
            except:
                driver.find_element_by_xpath('//*[@id="layerReplyYnSpan"]/div/div/div/div/ul/li[2]/a').click()


        if option_data['alarm_to_all'] == True:
            driver.find_element_by_xpath('//*[@id="all_open"]').click()
        else:
            driver.find_element_by_xpath('//*[@id="member_open"]').click()
        
        if option_data['allow_rightclick'] == True:
            pass
        else:
            driver.find_element_by_xpath('//*[@id="rclickspan"]').click()
            driver.find_element_by_xpath('//*[@id="layerRclickYnSpan"]/div/div/div/div/ul/li[2]/a').click()


        driver.find_element_by_xpath('//*[@id="cafewritebtn"]/strong').click()
        print('글등록완료')
        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 글등록 완료'.format(c_time))

        print('열린 탭:{}'.format(driver.window_handles))

    def upload_photo_process(self, item):
        """
        상품 대표이미지 업로드 
        """
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
        driver = self.driver
        wait = WebDriverWait(driver,20)
        buttons = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="iImage"]/a/strong')))
        buttons.click()
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

        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 등록할 글: {}'.format(c_time, item['title']))
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="pc_image_file"]').send_keys(item['img'])
        c_time = self.getFormattedCurrentTime()
        self.window.textBrowser.append('[{}] 대표 이미지 삽입 완료'.format(c_time))
        # 20초까지 기다림 
        wait = WebDriverWait(driver,20)
        # '올리기' 발견할 때까지 기다림
        buttons = wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '올리기')]")))
        try:
            buttons.click()
        except:
            driver.execute_script('arguments[0].click();',buttons)
    
    def del_samepost(self,title,address):
        try:
            driver = self.driver
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append('[{}] 중복 게시글 체크'.format(c_time))
            wait = WebDriverWait(driver, 3)
            driver.get(address)
            user_profile = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="cafe-info-data"]/ul/li[3]/p/a')))
            user_profile.click()
            my_posts = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ia-action-data"]/div[2]/ul/li[2]/span/strong/a')))
            my_posts.click()
            driver.switch_to_frame('cafe_main')
            driver.switch_to_frame('innerNetwork')

            soup = BeautifulSoup(driver.page_source,'html.parser')
            rows = soup.find_all('tr')
            
            # title = 'S급'
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
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append('[{}] 중복 게시글 제거 완료'.format(c_time))
        except:
            c_time = self.getFormattedCurrentTime()
            self.window.textBrowser.append('[{}] 중복 게시글 없음'.format(c_time))
        
    def getFormattedCurrentTime(self):
        now = time.localtime()
        c_time =  "%02d/%02d %02d:%02d:%02d" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        return c_time