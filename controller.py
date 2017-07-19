from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import random

from my_logger import *
from InstagramBotLibrary import *
from get_follow_counts import *

#Uncomment fo run without opening chrome window
display = Display(visible=0,size=(800,600))
display.start()

#set up mobile emulation
mobile_emulation = {"deviceName": "Apple iPhone 6"}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(desired_capabilities = chrome_options.to_capabilities())
#set up an actionchain for general keypresses
actions = ActionChains(driver)

#some constants
initial_followcount = 252
hashtags = open("hashtags.txt", "r").readlines()
randint(0,len(hashtags)-1)
#get the username/password
username = input("enter username: ")
password = input("enter password: ")

#login via the bot library
login(driver,username,password)

time.sleep(2)

#get rid of "save your password" because it might cause issues later
ActionChains(driver).send_keys(Keys.ESCAPE)

def do_the_unfollow():
    following = get_following(username)
    unfollow_limit = following - initial_followcount
    unfollow_all(driver, username, unfollow_limit)  

def do_the_follow():
    for tag in hashtags:
        log_message("info", "hashtag: "+tag)
        follow_and_like_from_hashtag(driver, tag)

def do_both():
    while(True):
        for i in range(0,50):
            hashtag = hashtags[randint(0,len(hashtags)-1)]
            log_message("info", "hashtag: "+hashtag)
            follow_and_like_from_hashtag(driver, hashtag)
            if(i%50 == 0):
                do_the_unfollow()
                do_the_unfollow()

#read in the args and decide what to do
if(len(sys.argv) > 1):
    if(sys.argv[1] == "follow"):
        do_the_follow()
    elif(sys.argv[1] == "unfollow"):
        for i in range(20):
            do_the_unfollow()
    else:
        log_message("error", "invalid you idiot")
else:
    log_message("info", "enter follow or unfollow argument fool, I'm just gonna go forever now")
    do_both()
