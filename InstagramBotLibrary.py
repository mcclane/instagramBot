import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import urllib.request
from random import randint
import logging

delay = 15#seconds
c = open("compliment_words.txt", "r")
w = open("whitelist.txt", "r")
cl = c.readlines()
wl = w.readlines()
c.close()
w.close()

def login(driver,username,password):
    driver.get("https://www.instagram.com/accounts/login/")
    login_box = driver.find_element_by_name("username")
    login_box.send_keys(username)
    password_box = driver.find_element_by_name("password")
    password_box.send_keys(password)
    password_box.send_keys(Keys.ENTER)
    return True

def follow(driver,person):
    driver.get("https://www.instagram.com/"+person)
    complete = False
    while(not complete):
        try:
            time.sleep(delay)
            follow_button = driver.find_elements_by_xpath("//*[contains(text(), 'Follow')]")[0]
            if(follow_button.text == "Follow"):
                follow_button.click()
                print("followed "+person)
            complete = True

        except IndexError:
            print("can't find follow button for "+person)
            return False
        except selenium.common.exceptions.StaleElementReferenceException:
            print("needs to load")
    return complete

def unfollow(driver,person):
    url = "https://www.instagram.com/"+person
    driver.get(url)
    time.sleep(delay)
    complete = False
    while(not complete):
        try:
            unfollow_button = driver.find_elements_by_xpath("//*[contains(text(), 'Following')]")[0]
            unfollow_button.click()
            time.sleep(delay/3)
            complete = True
        except IndexError:
            print("can't find unfollow button for "+person)
            return False
        except selenium.common.exceptions.ElementNotVisibleException: 
            print("element not visible")
        except selenium.common.exceptions.StaleElementReferenceException:
            print("needs to load")
    #print("unfollowed "+person)
    return True

def unfollow_all(driver, logger, my_username, unfollow_limit):
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
            logger.info("unfollowed "+usernames[i].text)
            time.sleep(20)
            driver.execute_script("window.scrollTo(0, "+str(52*unfollow_count)+");")
            time.sleep(1)

#        for button in unfollow_buttons:
#            button.send_keys(Keys.ENTER)
#            unfollow_count += 1
#            time.sleep(10)
#            print("unfollowed someone")
#            driver.execute_script("window.scrollTo(0, "+str(52*unfollow_count)+");")

def get_follow_num(driver, my_username):
    driver.get("https://www.instagram.com/"+my_username)
    time.sleep(2)
    return int(driver.find_elements_by_class_name("_bkw5z")[2].text)
    
def like_photo(driver, logger, link=None):
    if(link is not None):
        driver.get(link)
    complete = False
    while(not complete):
        try:
            like_button = driver.find_element_by_class_name("_tk4ba")
            like_button.click()
            logger.info("liked "+driver.current_url)
            return True
        except selenium.common.exceptions.NoSuchElementException:
            print("can't find like button!")
            return False
        except selenium.common.exceptions.StaleElementReferenceException:
            print("needs to load")
            time.sleep(1)

def get_links_from_hashtag(driver,hashtag):
    links = []
    url = "https://www.instagram.com/explore/tags/"+hashtag
    driver.get(url)
    time.sleep(delay)
    try:
        pictures = driver.find_elements_by_class_name("_t5r8b")
        for pic in pictures:
            links.append(pic.get_attribute("href"))
    except selenium.common.exceptions.NoSuchElementException:
        print("couldn't find picture classes in tag "+hashtag+", returning empty list")
    return links

def follow_from_photo(driver, logger, followed_dict,link=None):
    if(link is not None):
        driver.get(link)
    time.sleep(delay)
    try:
        follow_button = driver.find_element_by_class_name("_ah57t")
        username = driver.find_element_by_class_name("_4zhc5").text
        if(follow_button.text == "Follow"):
            follow_button.click()
            followed_dict[username] = ""
            logger.info("followed "+username)
            #print("followed "+username)
            time.sleep(1)
            return True
        else:
            return False
    except selenium.common.exceptions.NoSuchElementException:
        print("couldn't find follow button")
        return False

def comment(driver, logger, link=None):
    if(link is not None):
        driver.get(link)
    try:
        comment_sprite = driver.find_element_by_class_name("coreSpriteComment")
        comment_sprite.click()
        time.sleep(1)
        text_box = driver.find_element_by_class_name("_2hc0g")
        comment = "You are so "+cl[randint(0,len(cl)-1)].strip()+"! @joshuahowland"  
        for char in comment:
            text_box.send_keys(comment)
            time.sleep(0.1)
        time.sleep(1)
        text_box.send_keys(Keys.ENTER)
        logger.info("commented "+comment+" on "+driver.current_url)
        time.sleep(5)
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False
    
def follow_and_like_from_hashtag(driver, logger, hashtag,followed_dict):
    links = get_links_from_hashtag(driver,hashtag)
    i = 0
    for link in links:
        driver.get(link)
        time.sleep(1)
        follow_from_photo(driver, logger, followed_dict)
        time.sleep(2)
        like_photo(driver, logger)
        if(i%5 == 0):
            time.sleep(1)
            #comment(driver, logger)
        time.sleep(delay)
        i += 1

def follow_from_hashtag(driver,hashtag,followed_dict):
    links = []
    url = "https://www.instagram.com/explore/tags/"+hashtag
    driver.get(url)
    time.sleep(delay)
    try:
        pictures = driver.find_elements_by_class_name("_t5r8b")
        if(len(pictures) > 9):
            pictures = pictures[9:] #most popular users
    except selenium.common.exceptions.NoSuchElementException:
        print("couldn't find picture classes, aborting this hashtag follow session")
        return False
    for pic in pictures:
        links.append(pic.get_attribute("href"))
    for link in links:
        driver.get(link)
        time.sleep(delay)
        try:
            username = driver.find_element_by_class_name("_4zhc5").text
            follow(driver,username)
            followed_dict[username] = ""
            time.sleep(delay)
        except selenium.common.exceptions.NoSuchElementException:
            print("couldn't find element")
            continue
    return True
