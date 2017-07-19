import requests
import re
import time

from google_sheets import *
from my_logger import *

#get rid of annoying log message from requests library
import logging
logging.getLogger("requests").setLevel(logging.WARNING)

def get_follower():
    regex = '"followed_by": {"count": (\d+)}'
    followers = re.search(regex, text).group(1)
    return followers

def get_following():
    regex = '"follows": {"count": (\d+)}'
    following = re.search(regex, text).group(1)
    return following
