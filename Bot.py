from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import InstagramBotLibrary as insta
import logging
import sys

#Uncomment fo run without opening chrome window
display = Display(visible=0,size=(800,600))
display.start()

#set up the logger
#configure filename, level, and message format
logging.basicConfig(filename='general.log', level=logging.INFO, format='%(asctime)s %(message)s') #timestamp, message
#instantiate a root logger object 
logger = logging.getLogger()
#create an stdout logger to print the messages 
output = logging.StreamHandler(sys.stdout)
#set level for output (same as root logger)
output.setLevel(logging.INFO)
#set format for output logger
formatter = logging.Formatter('%(asctime)s %(message)s')
output.setFormatter(formatter)
#add the output to the root logger
logger.addHandler(output) #now log messages will also be printed to the terminal

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
    insta.unfollow_all(driver, logger, username, (follow_num - initial_followcount))  

def do_the_follow():
    hashtags = ["followback","custom","lfl","followers","hot","model","modifikasi","modify","path","Ill","racing","flf","likeforfollow","l4l","poto","cantik","sexy","hits","fff","kekinian","indonesia","motomorning","lizakoshy","lizzzak","lizzza","comedy","videos","vids","pics","pictures","love","instagood","photooftheday","tbt","beautiful","cute","me","happy","fashion","followme","follow","selfie","picoftheday","summer","friends","instadaily","girl","fun","tagsforlikes","smile","repost","igers","instalike","food","art","family","nature","likeforlike","style","nofilter","teamfollowback","lfl","likeback","likeforlike","f4f","follow4follow","followback","like4follow","follow","like4like","instalike","followforfollow","l4l"]

    followed_dict = {} # ***Tries**** to keep track of who the bot has followed so it can unfollow them
    for i in range(0,len(hashtags)):
        insta.follow_and_like_from_hashtag(driver, logger, hashtags[i], followed_dict)









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

