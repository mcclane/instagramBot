import requests
import time
import random
import sys
import re
import json

#my files
from logger import logger_2

#Session settings
DEVICE_SETTINGS = {
    'manufacturer'      : 'Xiaomi',
    'model'             : 'HM 1SW',
    'android_version'   : 18,
    'android_release'   : '4.3'
}
USER_AGENT = 'Instagram 10.26.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**DEVICE_SETTINGS)

#URLs
LOGIN_URL = "https://www.instagram.com/accounts/login/ajax/"
FOLLOW_URL = "https://www.instagram.com/web/friendships/%s/follow/"
UNFOLLOW_URL = "https://www.instagram.com/web/friendships/%s/unfollow/"
INBOX_URL = "https://www.instagram.com/direct_v2/inbox/"
HASHTAG_URL = "https://www.instagram.com/explore/tags/%s/?__a=1"
LIKE_URL = "https://www.instagram.com/web/likes/%s/like/"
COMMENT_URL = "https://www.instagram.com/web/comments/%s/add/"
FOLLOWING_URL = "https://www.instagram.com/graphql/query/"

class Bot(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        #create a requests session to save cookies
        self.s = requests.Session()
        self.logger = logger_2(self.username)
        self.logger.log_login("attempt")
        self.login()

    def login(self):
        #try to log in
        self.s.cookies.update({
            'sessionid': '',
            'mid': '',
            'ig_pr': '1',
            'ig_vw': '1920',
            'csrftoken': '',
            's_netword': '',
            'ds_user_id': ''
        })
        login_post = {
            'username': self.username,
            'password': self.password
        }
        self.s.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': USER_AGENT,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })
        r = self.s.get("https://www.instagram.com/")
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5*random.random())
        login = self.s.post(
            LOGIN_URL, data=login_post, allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        csrftoken = login.cookies['csrftoken']
        time.sleep(5 * random.random())
        if(login.status_code == 200):
            r = self.s.get("https://www.instagram.com/")
            self.id = re.search("\"id\": \"(\d+)\"", r.text).group(1)
            finder = r.text.find(self.username)
            if(finder != -1):
                self.logger.log_login("success")
            else:
                self.logger.log_login("auth_unsuccessful")
                sys.exit()
        else:
            self.logger.log_login(self.username, "auth_error:%d"%login.status.code)
            sys.exit()

    def follow(self, user_id):
        follow = self.s.post(FOLLOW_URL % (user_id))
        self.logger.log_follow("follow", user_id, follow.text)

    def unfollow(self, user_id):
        unfollow = self.s.post(UNFOLLOW_URL % (user_id))
        self.logger.log_follow("unfollow", user_id, unfollow.text)

    def like(self, media_id):
        like = self.s.post(LIKE_URL % (media_id))
        self.logger.log_like("like_photo", media_id, like.text);

    def comment(self, comment_text, media_id):
        comment = self.s.post(COMMENT_URL % (media_id), data={"comment_text":comment_text})
        self.logger.log_comment("write_comment", media_id, comment.text)

    def get_media_from_hashtag(self, hashtag):
        #scrape a hashtag for a list of media dicts. Keys I need to know: 'id' 'owner':'id'
        hashtag = self.s.post(HASHTAG_URL % (hashtag))
        return json.loads(hashtag.text)['tag']['media']['nodes']

    #not done and only works for tlanews account because of id right now
    def get_following(self):
        data = {
            'query_id': 17874545323001329,
            'variables': "{\"id\":\"6116209680\",\"first\":1985}",
        }
        req = self.s.post(FOLLOWING_URL, data=data)
        f = open("following_list_json.txt", "w")
        f.write(req.text)
        return req.text

    #not done and only works for me
    def unfollow_bulk(self):
        with open("id_list.txt") as f:
            for line in f.readlines():
                self.unfollow(int(line.strip()))
                time.sleep(65)
