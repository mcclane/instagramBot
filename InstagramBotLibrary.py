import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request
import random

delay = 15#seconds

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

    print("unfollowed "+person)
    return complete

def like_photo(driver, link=None):
    if(link is not None):
        driver.get(link)
    complete = False
    while(not complete):
        try:
            like_button = driver.find_element_by_class_name("_tk4ba")
            like_button.click()
            complete = True
        except selenium.common.exceptions.NoSuchElementException:
            print("can't find like button!")
            break
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


def follow_from_photo(driver,followed_dict,link=None):
    if(link is not None):
        driver.get(link)
    time.sleep(delay)
    try:
        follow_button = driver.find_element_by_class_name("_ah57t")
        username = driver.find_element_by_class_name("_4zhc5").text
        if(follow_button.text == "Follow"):
            follow_button.click()
            followed_dict[username] = ""
            print("followed "+username)
            time.sleep(1)
            return True
        else:
            return False
    except selenium.common.exceptions.NoSuchElementException:
        print("couldn't find follow button")
        return False
    
def follow_and_like_from_hashtag(driver,hashtag,followed_dict):
    links = get_links_from_hashtag(driver,hashtag)
    for link in links:
        driver.get(link)
        time.sleep(2)
        like_photo(driver)
        time.sleep(1)
        follow_from_photo(driver,followed_dict)
        time.sleep(delay)


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



        
