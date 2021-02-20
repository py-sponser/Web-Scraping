from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time, threading, math

class InstagramBot:
    def __init__(self,username,password):
        """Getting credentials and launching the browser"""
        self.username = username # getting username to login
        self.password = password # getting password to login
        self.driver = webdriver.Firefox() # creating an object of browser driver + opening that browser (Firefox)
        # self.driver = webdriver.Chrome()
    
    def closeBrowser(self):
        """Closes the automated browser"""
        self.driver.close()

    
    def login(self):
        """Login to your account"""
        # username_field (name="username")
        # password_field (name="password")
        driver  = self.driver # creating object of browser driver throught self.driver
        driver.get("https://www.instagram.com/") # getting instagram page
        time.sleep(5) # sleep 
        username_field = driver.find_element_by_xpath("//input[@name='username']") # finding input for username
        username_field.clear() # clear it
        username_field.send_keys(self.username) # write given username
        
        password_field = driver.find_element_by_xpath("//input[@name='password']") # finding input for password
        password_field.clear() # clear it
        password_field.send_keys(self.password) # write given password
        password_field.send_keys(Keys.ENTER) # click enter to login
        time.sleep(4) # sleep
        not_now_btn = driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click() # click on not now button

    def follow_from_pages(self):
        """Follow all people that follow specific page you provide its name"""
        time.sleep(3)
        page_name = str(input("[+] Enter page name:\n>  ")) # enter the page name
        page_url = f"https://www.instagram.com/{page_name}" # save the page url to page_url variable
        driver = self.driver # creating object of browser driver throught self.driver
        driver.get(page_url) # open the page
        time.sleep(2) # sleep
        number_of_followers_tag = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span") # getting tag of followers by xpath
        number_of_followers = str(number_of_followers_tag.get_attribute("title")) # getting the value of tag attribute 'title'
        if "," in number_of_followers: # if "," in number_of_followers
            number_of_followers = number_of_followers.replace(",","") # replacing ',' by ''
        number_of_followers = int(number_of_followers) # converting the value to integar

        driver.find_element_by_xpath(f"//a[contains(@href,'/{page_name}/followers')]").click() # getting the page window of its followers
        time.sleep(2) # sleep

    
        followers_dialog = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]") # getting the scrolling div
        count = 1 # initializing count with 1
        while True: # infinte loop
            time.sleep(1) # sleep
            followers_dialog.send_keys(Keys.PAGE_DOWN) # scroll down
            followed = None # initializing variable with None
            for i in range(count,number_of_followers): # for loop repeating {number_of_followers} times and starting with value of count
                try: # try
                    if followed == True: # if iterated user is already followed or Requested,
                        time.sleep(1) # let time of sleep so low
                    else: # if not
                        time.sleep(5) # sleep for required time to let page get loaded
                    followed = False # assign followed to False, in case it was assigned to True
                    if driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").text == "Requested" or driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").text == "Following": # if user is already requested or followed
                        followed = True # let followed be True
                        continue # continue the loop.
                    follow_btns = driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").click() # click on current follow button
                    time.sleep(2) # sleep
                    if driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").text == "Follow": # if button text is still Follow
                        time.sleep(3) # sleep
                        follow_btns = driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/button").click() # try to click on Follow button again
                    print(count)
                    # if count == 60:
                    #     time.sleep(3600)
                    if i == number_of_followers: # if i is = number of followers, no more people to follow
                        print("[+] You have followed all followers of the page.\n[+] Quitting ...") # message before quitting the app
                        break # quit
                    count = i+1 # incrementing count by 1
                except: # if there was any error
                    count = i # let loop start with value of i with count. (assign i to count)
            

    def messageTo_my_followings(self):
        """Send message to all of people you follow"""
        driver = self.driver # initializing a browser driver object
        driver.get(f"https://www.instagram.com/{self.username}/") # loading the profile page of loggedin user

        number_of_followings = driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span")[0].text # getting current number of followings
        if "," in str(number_of_followings): # if number is 111,12
            number_of_followings = number_of_followings.replace(",","") # replace ',' with ''
        elif "k" in str(number_of_followings): # if number is 15k
            number_of_followings = number_of_followings.replace("k","000") # number will be 15000
        print(number_of_followings)
        number_of_followings = int(number_of_followings) convert the string number to integar
        driver.find_element_by_xpath(f"//a[contains(@href,'/{self.username}/following/')]").click() # clicking on following button to show people I follow
        
        for i in range(1,number_of_followings+1): # for loop repeating {number_of_followings} times.
            time.sleep(2) # sleep
                                                              
            followed_profile = driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/div[1]/div/div/span/a").text # getting username of someone I follow
            time.sleep(2)
            driver.execute_script(f"window.open('https://www.instagram.com/{followed_profile}/','_blank');") # opening a new tab with loading profile page of the someone
            time.sleep(6)
            message_btn = driver.find_element_by_xpath("//button[contains(text(),'Message']").click() # click on the message button
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
bot.messageTo_my_followings()
bot.closeBrowser()
