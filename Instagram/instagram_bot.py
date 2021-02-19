from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time, threading, math

class InstagramBot:
    def __init__(self,username,password):
        """Getting credentials and launching the browser"""
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.Chrome()
    
    def closeBrowser(self):
        self.driver.close()

    
    def login(self):
        # username_field (name="username")
        # password_field (name="password")
        driver  = self.driver   
        driver.get("https://www.instagram.com/")
        time.sleep(5)
        username_field = driver.find_element_by_xpath("//input[@name='username']")
        username_field.clear()
        username_field.send_keys(self.username)
        
        password_field = driver.find_element_by_xpath("//input[@name='password']")
        password_field.clear()
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(4)
        not_now_btn = driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
        not_now_btn.click()

    def follow_from_pages(self):
        time.sleep(3)
        page_name = str(input("[+] Enter page name:\n>  "))
        page_url = f"https://www.instagram.com/{page_name}"
        driver = self.driver
        driver.get(page_url)
        time.sleep(2)
        number_of_followers_tag = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        number_of_followers = str(number_of_followers_tag.get_attribute("title"))
        number_of_followers = number_of_followers.replace(",","")
        number_of_followers = int(number_of_followers)

        driver.find_element_by_xpath(f"//a[contains(@href,'/{page_name}/followers')]").click()
        time.sleep(2)

    
        followers_dialog = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        count = 1
        end = 10
        while True:
            time.sleep(1)
            followers_dialog.send_keys(Keys.PAGE_DOWN)
            followed = None
            for i in range(count,number_of_followers):
                try:
                    if followed == True:
                        time.sleep(1)
                    else:
                        time.sleep(5)
                    followed = False
                    if driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").text == "Requested" or driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").text == "Following":
                        followed = True
                        continue
                    follow_btns = driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").click()
                    time.sleep(2)
                    if driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").text == "Follow":
                        time.sleep(3)
                        follow_btns = driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").click()
                    print(count)
                    # if count == 60:
                    #     time.sleep(3600)
                    if i == number_of_followers:
                        print("[+] You have followed all followers of the page.\n[+] Quitting ...")
                        break
                    count = i+1
                except: 
                    count = i
            

    def like_my_followings(self):
        driver = self.driver
        driver.get(f"https://www.instagram.com/{self.username}/")

        number_of_followings = driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span")[0].text
        if "," in str(number_of_followings):
            number_of_followings = number_of_followings.replace(",","")
        print(number_of_followings)
        number_of_followings = int(number_of_followings)
        driver.find_element_by_xpath(f"//a[contains(@href,'/{self.username}/following/')]").click() # clicking on following button to show people I follow
        
        for i in range(1,number_of_followings+1):
            time.sleep(2)
                                                              
            followed_profile = driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/div[1]/div/div/span/a").text # getting username of someone I follow
            time.sleep(2)
            driver.execute_script(f"window.open('https://www.instagram.com/{followed_profile}/','_blank');") # opening a new tab with loading the link of user
            time.sleep(6)
            # driver.find_elements_by_xpath("//button[contains(text(), 'Message')]").click() # click on the message button
            message_btn = driver.find_element_by_xpath("//button[contains(text(),'Message']").click()
            print(message_btn)
            time.sleep(3) # sleep some time
            message_field = driver.find_elements_by_xpath(f"/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")[0] # click on text area (message field)
            message_field.clear() # clear it
            message_field.send_keys("Hi") # write the message
            message_field.send_keys(Keys.ENTER) # click enter (send the message)
            time.sleep(1)
            driver.execute_script('''window.close()''') # closing the opened tab


bot = InstagramBot("username","password")
bot.login()
# bot.follow_from_pages()
bot.like_my_followings()
bot.closeBrowser()
