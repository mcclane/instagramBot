from google_sheets import *
from InstagramBotLibrary import *

from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

from InstagramBotLibrary import *

#Uncomment fo run without opening chrome window
display = Display(visible=0,size=(800,600))
display.start()

#set up mobile emulation
mobile_emulation = {"deviceName": "Apple iPhone 6"}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(desired_capabilities = chrome_options.to_capabilities())
#set up an actionchain for general keypresses

username = input("enter username: ")
password = input("enter password: ")

login(driver, username, password)

upload_counter = 1
data = []
while(True):
    following_count = get_follow_num(driver, username)
    followers_count = get_follower_count(driver, username)
    data.append([time.time(), followers_count, following_count])

    if(upload_counter%10 == 0):
        upload(data)
        data = []
        print("uploaded some data!")

    upload_counter += 1

     

