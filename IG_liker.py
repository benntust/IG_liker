from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

class InstagramBot:

    def __init__(self,username,password):
        self.username=username
        self.password=password

    def closeBrowser(self):
        driver.close()
    
    def login(self):
        driver.get("https://www.instagram.com/")
        #等username元素出現，至多30sec
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
        #定位
        username_input = driver.find_elements_by_name('username')[0]
        password_input = driver.find_elements_by_name('password')[0]
        #輸入帳號密碼
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        #等login button可以被按下
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="loginForm"]/div/div[3]/button/div')))
        #定位
        login_click = driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')[0]
        #按下login button
        login_click.click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/div/div/div/button')))
        '''dontcare1=driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')[0]
        dontcare1.click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div/div/div/div[3]/button[2]')))
        dontcare2=driver.find_elements_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')[0]
        dontcare2.click()'''
    
    def like_photo(self, hashtag):
        print('loading...')
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(1)
        # gathering photos
        pic_hrefs = []
        for i in range(1, 5):
            try:
                # scroll webpage
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                #'.com/p/' is a component of post address
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]            
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            except Exception:
                continue
        print("collect",str(len(pic_hrefs)),"posts...")    

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            # scroll webpage
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                #like_button = driver.find_elements_by_class_name('fr66n')
                like_button = driver.find_elements_by_xpath(".//*[@class='fr66n']/button")
                #print(like_button)
                like_button[0].click()
                time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(2)
        print("done")

if __name__ == "__main__":
    username=input('account:')
    password=input('password:')
    hashtags = input('hashtag:')
    driver=webdriver.Chrome("./chromedriver.exe")
    me=InstagramBot(username, password)
    me.login()
    me.like_photo(hashtags)
    me.closeBrowser()