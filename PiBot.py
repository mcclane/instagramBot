from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import PiInstagramBotLibrary as insta
#Uncomment fo run without opening chrome window
display = Display(visible=0,size=(800,600))
display.start()

#set up mobile emulation
#mobile_emulation = {"deviceName": "Google Nexus 5"}
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
#driver = webdriver.Chrome(desired_capabilities = chrome_options.to_capabilities())
#set up an actionchain for general keypresses
driver = 
actions = ActionChains(driver)

username = input("enter username: ")
password = input("enter password: ")

insta.login(driver,username,password)

time.sleep(2)
hashtags = ["love","instagood","photooftheday","tbt","beautiful","cute","me","happy","fashion","followme","follow","selfie","picoftheday","summer","friends","instadaily","girl","fun","tagsforlikes","smile","repost","igers","instalike","food","art","family","nature","likeforlike","style","nofilter","teamfollowback","lfl","likeback","likeforlike","f4f","follow4follow","followback","like4follow","follow","like4like","instalike","followforfollow","l4l"]

followed_dict = {} #keeps track of who the bot has followed so it can unfollow them
for i in range(0,len(hashtags)):
    insta.follow_and_like_from_hashtag(driver,hashtags[i],followed_dict)
    if(i%4 == 0):
        print("unfollowing people")
        for person in list(followed_dict): #make a copy of the dict so we can delete things from the real dict
            insta.unfollow(driver,person)
            del followed_dict[person] 
            time.sleep(15)
#make an attempt to clean up 
for person in list(followed_dict): #make a copy of the dict so we can delete things from the real dict
    insta.unfollow(driver,person)
    del followed_dict[person] 
    time.sleep(15)



