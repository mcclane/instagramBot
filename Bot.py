from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import InstagramBotLibrary as insta
import sys
from my_logger import *

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

initial_followcount = 371
username = input("enter username: ")
password = input("enter password: ")

insta.login(driver,username,password)

time.sleep(2)

ActionChains(driver).send_keys(Keys.ESCAPE)

def do_the_unfollow():
    follow_num = insta.get_follow_num(driver, username)
    insta.unfollow_all(driver, username, (follow_num - initial_followcount))  

def do_the_follow():
    hashtags = ["followback","custom","lfl","followers","hot","model","modifikasi","modify","path","Ill","racing","flf","likeforfollow","l4l","poto","cantik","sexy","hits","fff","kekinian","indonesia","motomorning","lizakoshy","lizzzak","lizzza","comedy","videos","vids","pics","pictures","love","instagood","photooftheday","tbt","beautiful","cute","me","happy","fashion","followme","follow","selfie","picoftheday","summer","friends","instadaily","girl","fun","tagsforlikes","smile","repost","igers","instalike","food","art","family","nature","likeforlike","style","nofilter","teamfollowback","lfl","likeback","likeforlike","f4f","follow4follow","followback","like4follow","follow","like4like","instalike","followforfollow","l4l"]

    followed_dict = {} # ***Tries**** to keep track of who the bot has followed so it can unfollow them
    for tag in hashtags:
        log_message("info", "hashtag: "+tag)
        insta.follow_and_like_from_hashtag(driver, tag, followed_dict)










#read in the args and decide what to do
if(len(sys.argv) > 1):
    if(sys.argv[1] == "follow"):
        do_the_follow()
    elif(sys.argv[1] == "unfollow"):
        do_the_unfollow()
    else:
        print("invalid you idiot")
else:
    print("enter follow or unfollow argument fool")

