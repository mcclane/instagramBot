import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import urllib.request
from random import randint
from my_logger import *

delay = 15#seconds

#get the words for generating comments 
c = open("compliment_words.txt", "r")
v = open("verblist.txt", "r")
n = open("nounlist.txt", "r")
cl = c.readlines()
vl = v.readlines()
nl = n.readlines()
c.close()
v.close()
n.close()

#get the whitelist (users I don't want to unfollow)
w = open("whitelist.txt", "r")
wl = w.readlines()
w.close()
shoutout_users = ["joshuahowland", "mcclane.howland", "daniel___yoon"]

def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    login_box = driver.find_element_by_name("username")
    login_box.send_keys(username)
    password_box = driver.find_element_by_name("password")
    password_box.send_keys(password)
    password_box.send_keys(Keys.ENTER)
    log_message("info", "logged in to "+username)
    return True

def follow(driver, person): #individual person
    driver.get("https://www.instagram.com/"+person)
    complete = False
    while(not complete):
        try:
            time.sleep(delay)
            follow_button = driver.find_elements_by_xpath("//*[contains(text(), 'Follow')]")[0]
            if(follow_button.text == "Follow"):
                follow_button.click()
                log_message("info", "followed "+person)
            complete = True

        except IndexError:
            log_message("info", "can't find follow button for "+person)
            return False
        except selenium.common.exceptions.StaleElementReferenceException:
            print("needs to load")
    return complete

def unfollow(driver, person): #individual person
    url = "https://www.instagram.com/"+person
    driver.get(url)
    time.sleep(delay)
    complete = False
    while(not complete):
        try:
            unfollow_button = driver.find_elements_by_xpath("//*[contains(text(), 'Following')]")[0]
            unfollow_button.click()
            time.sleep(delay/3)
            log_message("info", "unfollowed "+person)
            complete = True
        except IndexError:
            log_message("info", "can't find unfollow button for "+person)
            return False
        except selenium.common.exceptions.ElementNotVisibleException: 
            log_message("error", "unfollow button not visible for user "+person)
        except selenium.common.exceptions.StaleElementReferenceException:
            print("needs to load")
    return True

def unfollow_all(driver, my_username, unfollow_limit): #(unfollow_limit) persons from my page
    unfollow_count = 0
    while(True):
        if(unfollow_count >= unfollow_limit):
            break
        driver.get("https://www.instagram.com/"+my_username)
        time.sleep(2)
        follow_page_link = driver.find_element_by_xpath("//*[contains(text(), 'following')]")
        follow_page_link.click()
        time.sleep(2)
        unfollow_buttons = driver.find_elements_by_class_name("_ah57t")
        usernames = driver.find_elements_by_class_name("_4zhc5")
        for i in range(len(unfollow_buttons)):
            if(usernames[i].text in wl):
                continue
            unfollow_buttons[i].send_keys(Keys.ENTER)
            unfollow_count += 1
            log_message("info", "unfollowed "+usernames[i].text)
            time.sleep(20)
            driver.execute_script("window.scrollTo(0, "+str(52*unfollow_count)+");")
            time.sleep(1)

def get_follow_num(driver, my_username): #scrape how many people I follow
    driver.get("https://www.instagram.com/"+my_username)
    time.sleep(3)
    return int(driver.find_elements_by_class_name("_bkw5z")[2].text)

def get_follower_count(driver, my_username): #scrape how many people I follow
    driver.get("https://www.instagram.com/"+my_username)
    time.sleep(3)
    return int(driver.find_elements_by_class_name("_bkw5z")[1].text)
   
def like_photo(driver, link=None): 
    if(link is not None):
        driver.get(link)
    complete = False
    while(not complete):
        try:
            like_button = driver.find_element_by_class_name("_tk4ba")
            like_button.click()
            log_message("info", "liked "+driver.current_url)
            return True
        except selenium.common.exceptions.NoSuchElementException:
            print("can't find like button!")
            return False
        except selenium.common.exceptions.StaleElementReferenceException:
            print("needs to load")
            time.sleep(1)

def get_links_from_hashtag(driver, hashtag): #scrape photo links from a hashtag
    links = []
    url = "https://www.instagram.com/explore/tags/"+hashtag
    driver.get(url)
    time.sleep(delay)
    try:
        pictures = driver.find_elements_by_class_name("_t5r8b")
        for pic in pictures:
            links.append(pic.get_attribute("href"))
    except selenium.common.exceptions.NoSuchElementException:
        log_message("error", "couldn't find picture classes in tag "+hashtag+", returning empty list")
    return links

def follow_from_photo(driver): #follow directly from a photo (that the driver is already on)
    time.sleep(delay)
    try:
        follow_button = driver.find_element_by_class_name("_ah57t")
        username = driver.find_element_by_class_name("_4zhc5").text
        if(follow_button.text == "Follow"):
            follow_button.click()
            log_message("info", "followed "+username)
            #print("followed "+username)
            time.sleep(1)
            return True
        else:
            return False
    except selenium.common.exceptions.NoSuchElementException:
        log_message("info", "couldn't find something when trying to follow user")
        return False

def comment(driver, link=None):
    if(link is not None):
        driver.get(link)
    try:
        comment_sprite = driver.find_element_by_class_name("coreSpriteComment")
        comment_sprite.click()
        time.sleep(1)
        text_box = driver.find_element_by_class_name("_2hc0g")
        comment = generate_comment() 
        for char in comment:
            text_box.send_keys(comment)
            time.sleep(0.1)
        time.sleep(1)
        text_box.send_keys(Keys.ENTER)
        log_message("info", "commented "+comment+" on "+driver.current_url)
        time.sleep(5)
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False
    
def follow_and_like_from_hashtag(driver, hashtag):
    links = get_links_from_hashtag(driver,hashtag)
    i = 0
    for link in links:
        driver.get(link)
        time.sleep(1)
        follow_from_photo(driver)
        time.sleep(2)
        like_photo(driver)
        if(i%5 == 0):
            time.sleep(1)
            #comment(driver)
        time.sleep(delay)
        i += 1

def generate_comment():
    n1 = nl[randint(0,len(nl)-1)].strip()
    n2 = nl[randint(0,len(nl)-1)].strip()
    v1 = vl[randint(0,len(vl)-1)].strip()
    c1 = cl[randint(0,len(cl)-1)].strip()
    user = shoutout_users[randint(0,len(shoutout_users)-1)]
    return "The "+n1+"s "+v1+" the "+n2+". You are so "+c1+"! @"+user


