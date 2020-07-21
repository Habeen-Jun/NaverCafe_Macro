from selenium import webdriver
import time
from selenium.webdriver.common import keys
from bs4 import BeautifulSoup


class Naver_Posting:
    
    def __init__(self,window,ID,PW):
        self.window = window
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
        #options.add_argument("headless")
        driver = webdriver.Chrome('chromedriver',options=options)
        # self.driver = self.NaverLogin(driver,'junhabeen','wjsgkqls123')
        self.driver = self.NaverLogin(driver,ID,PW)
        self.get_category()

        self.stop_process = False 
        

    def post(self, interval, option_data, item_list):
        """
        option_data = 작업실행 시 체크리스트
        item_list = 아이템 딕셔너리 담은 리스트

        """

        if self.stop_process == False:

            self.window.textBrowser.append("총 {} 개 게시글을 등록합니다.".format(str(len(item_list))))
            print("총 {} 개 게시글을 등록합니다.".format(str(len(item_list))))
            for item in item_list:

                self.window.textBrowser.append('작업대기시간: {}'.format(str(interval)))
                print(item)
            

                driver = self.driver
                
                # driver.get('https://cafe.naver.com/realseller')
                driver.get('https://cafe.naver.com/4uloveme.cafe')
                driver.get('https://cafe.naver.com/4uloveme.cafe')

                try:
                    driver.find_element_by_xpath('//*[@id="seOneArticleFormBannerCloseBtn"]').click()
                except:
                    pass
                

                time.sleep(2)

                # 카페 글등록 클릭
                sample = driver.find_element_by_xpath('//*[@id="cafe-info-data"]/div[2]/a')
                driver.execute_script("arguments[0].click();", sample)
                driver.implicitly_wait(3)

                # 카페 메인 프레임 진입 
                driver.switch_to.frame("cafe_main")

                # 카테고리 선택
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="boardCategory"]').click()
                category_num = str(int(item['category_id'])+1)
                driver.find_element_by_xpath('//*[@id="boardCategory"]/option['+category_num+']').click()
                time.sleep(2)


                try:
                    alert = driver.switch_to_alert()
                    alert.accept()
                    # 경고메세지가 뜬 건 판매글임
                    print('alert accepted')
                    selling_post = 1
                except:
                    selling_post = 0
                
                if selling_post == 1:
                    self.window.textBrowser.append('판매글 게시판')
                    self.Selling_Post_Process(option_data,item)
                else:
                    print('no alert')
                    self.window.textBrowser.append('일반 게시판')
                    self.Post_Process(option_data,item)

                # 각 게시물 간 interval
                time.sleep(int(interval))


    def Selling_Post_Process(self, option_data, item):
        time.sleep(0.5)
        driver = self.driver
        try:
            driver.find_element_by_xpath('//*[@id="main-area"]/div[3]/div[1]/div/a[2]/img').click()
            driver.find_element_by_xpath('//*[@id="subject"]').click()
        except:
            pass
        # driver.find_element_by_xpath('//*[@id="main-area"]/div[3]/div[1]/div/a[2]/img')
        time.sleep(2)
        # 대표이미지 삽입

        driver.find_element_by_xpath('//*[@id="iImage"]/a/strong').click()
        time.sleep(3)
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
        driver.find_element_by_xpath('/html/body/div[3]/header/div[2]/button').click()

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
            driver.find_element_by_xpath('//*[@id="layerRclickYnSpan"]/div/div/div/div/ul/li[2]/a').click()

        

        
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



        #img_insert b/w body tag 
        img_element = """<img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20160202_248%2Fceofus_1454363629379LVbMf_JPEG%2F20160201_190734.jpg&amp;type=b400" class="_img" alt="파이썬 자바 C 코딩 커뮤니티를 만들어 가는 겨울은 뜨겁게 코딩을 하며; ^^ @카페 다니엘 | 블로그" onerror="var we=$Element(this); we.addClass('bg_nimg'); we.attr('alt','이미지준비중'); we.attr('src','data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');" data-width="550" data-height="412" style="height: 176.175px; width: 235.185px; left: 0px; top: 0px; zoom: 1; opacity: 1;">"""
        self.insert_img(img_element)


        driver.switch_to.default_content()
        driver.switch_to.frame("cafe_main")

        driver.find_element_by_xpath('//*[@id="cafewritebtn"]/strong').click()
        self.window.textBrowser.append('글등록완료')
        print('글등록완료')
        time.sleep(2)

        print('열린 탭:{}'.format(driver.window_handles))
            

    def Post_Process(self,option_data, item):
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


    def NaverLogin(self,driver,ID,PW):
            url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
            # 네이버 로그인 url 접속
            driver.get(url)
            # 캡챠(봇 감지) 우회를 위해 execute_script 함수로 id, pw 입력
            driver.execute_script("document.getElementsByName('id')[0].value='" + ID + "'")
            time.sleep(0.5)
            driver.execute_script("document.getElementsByName('pw')[0].value='" + PW + "'")
            time.sleep(0.5)
            # 로그인 버튼을 찾아 클릭
            driver.find_element_by_xpath('//*[@id="log.login"]').click()
            print('login success')
            # 새로운 창을 띄우지 않기 위해서 driver 객체를 리턴
            return driver


    def insert_img(self,img_element):
            # 쌍 따옴표를 홀 따옴표로 변환 
            img_str = img_element.replace('"',"'")
            node = self.driver.find_element_by_xpath("/html/body")
            img_script = "arguments[0].insertAdjacentHTML('afterbegin', "+'"'+img_str+'"'+")"
            self.driver.execute_script("arguments[0].insertAdjacentHTML('afterbegin', "+'"'+img_str+'"'+")",node)

    def get_category(self):
        driver = self.driver
        driver.get('https://cafe.naver.com/4uloveme.cafe')
        driver.get('https://cafe.naver.com/4uloveme.cafe')


        try:
            driver.find_element_by_xpath('//*[@id="seOneArticleFormBannerCloseBtn"]').click()
        except:
            pass

         # 카페 글등록 클릭
        sample = driver.find_element_by_xpath('//*[@id="cafe-info-data"]/div[2]/a')
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
   
    def stop_process(self):
        self.stop_process = True

        