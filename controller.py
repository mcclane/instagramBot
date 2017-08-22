from bot import Bot
from getpass import getpass
from random import randint
import time

###################
## Constants
###################
DELAY = 120
PIPE_DEPTH = 200
HOW_MANY_TAGS = 1000

#####################
## Get the resources
#####################
cs = open("resources/compliment_strings.txt", "r")
h = open("resources/hashtags.txt", "r")
csl = cs.readlines()
hl = h.readlines()
cs.close()
h.close()


###################
## Create the bot
###################
b = Bot(input("USERNAME: "), getpass("PASSWORD: "))

time.sleep(2)

followed_list = []
for i in range(HOW_MANY_TAGS):
    #get the media for a random hashtag
    tag = hl[randint(0,len(hl)-1)].strip()
    media = b.get_media_from_hashtag(tag)
    #iterate through, like all and comment on a few
    for i in range(len(media)):
        b.like(media[i]['id'])
        time.sleep(1)
        if(i == len(media)/2):
            b.comment(csl[randint(0, len(csl)-1)], media[i]['id'])
            time.sleep(1)
        #b.follow(media[i]['owner']['id'])
        time.sleep(1)
        #followed_list.append(media[i]['owner']['id'])
        if(len(followed_list) > PIPE_DEPTH):
            b.unfollow(followed_list[0])
            followed_list.pop(0)
        time.sleep(DELAY)

#clean up
for user in followed_list:
    b.unfollow(user)
