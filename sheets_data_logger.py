import requests
import re
import time

from google_sheets import *
from my_logger import *

#get rid of annoying log message from requests library
import logging
logging.getLogger("requests").setLevel(logging.WARNING)


upload_counter = 1
data = []
while(True):
    try:
        r = requests.get("https://www.instagram.com/mcclane.howland")
        text = r.text
        regex = '"followed_by": {"count": (\d+)}'
        followers = re.search(regex, text).group(1)
        regex = '"follows": {"count": (\d+)}'
        following = re.search(regex, text).group(1)
        data.append([time.time(), followers, following])
    except Exception:
        log_message("error", "exception in sheets_data_logger.py")
        pass

    if(upload_counter%50 == 0):
        upload(data)
        data = []
        log_message("info", "uploaded some data to google sheets")

    upload_counter += 1
    time.sleep(2)

     

