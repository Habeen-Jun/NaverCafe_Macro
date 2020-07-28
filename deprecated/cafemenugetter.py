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

