from bot import Bot
import follower_accounting as fa
from getpass import getpass
from random import randint
import time
import argparse

'''
Main runner class that reads in flags and starts the bot. All flags optional:
    Sample Invocation:
        python3 controller.py  --hashtag_type=surfing --number_of_tags=20
    All arguments:
        hashtag_type : grouping of hashtags to randomly visit posts from
        delay : time (rough) between each bot action
        pipe_depth : maximum number of account should follow
        number_of_tags : number of hashtags bot will exhaustively visit
        cycle: follow number of users passed in, then unfollow them all
        username: username, if not passed in ask for user input
        password: password, if not passed in ask for user input
'''
def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('instruction', type=str)
    parser.add_argument('--hashtag_type', type=str, default='big_list', help='Options: big_list, surfing, travel, memes')
    parser.add_argument('--delay', type=int, default=120)
    parser.add_argument('--pipe_depth', type=int, default=200)
    parser.add_argument('--number_of_tags', type=int, default=1000)
    parser.add_argument('--cycle', type=int, default=None)
    parser.add_argument('--username', type=str, default=None)
    parser.add_argument('--password', type=str, default=None)
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--mass_unfollow', type=int, default=-1)
    parser.add_argument('--WayneWashington', action='store_true')
    args = parser.parse_args()

    # Get the resources
    cs = open("resources/compliment_strings.txt", "r")
    compliments = cs.readlines()
    cs.close()

    #username/password
    if(args.username == None): username = input("Username: ")
    else: username = args.username
    if(args.password == None): password = getpass()
    else: password = args.password
    #hashtag list
    if args.hashtag_type == 'big_list':
        h = open("resources/hashtags.txt", "r")
    elif args.hashtag_type == 'surfing':
        h = open("resources/surfing_hashtags.txt", "r")
    elif args.hashtag_type == 'travel':
        h = open("resources/travel_hashtags.txt", "r")
    elif args.hashtag_type == 'memes':
        h = open("resources/meme_hashtags.txt", "r")
    else:
        raise ValueError('Argument hashtag_type %s invalid.'%args.hashtag_type)
    hashtags = h.readlines()
    h.close()

    #what the bot will do
    if(args.mass_unfollow != -1):
        print("Starting mass unfollow")
        mass_unfollow(username, password, args.mass_unfollow)
    elif(args.cycle != None):
        print("starting cycle")
        run_cycle(username, password, args.delay, args.cycle, compliments, hashtags)
    elif(args.clean):
        print("starting clean")
        clean(username, password, args.delay)
    elif(args.WayneWashington):
        print("starting the wayne washington - no following!")
        WayneWashington(username, password, args.delay, hashtags, compliments)
    else:
        print("starting pipeline")
        run_bot(username, password, args.delay, args.pipe_depth, args.number_of_tags, compliments, hashtags)

def run_bot(username, password, delay, pipe_depth, number_of_tags, compliments, hashtags):
    # Create the bot
    b = Bot(username, password)
    time.sleep(2)
    followed_list = []
    for i in range(number_of_tags):
        try:
            #get the media for a random hashtag
            tag = hashtags[randint(0,len(hashtags)-1)].strip()
            media = b.get_media_from_hashtag(tag)
            #iterate through, like all and comment on a few
            for i in range(len(media)):
                b.like(media[i]['id'], tag)
                time.sleep(1)
                if(randint(0,9) == 0):
                    b.comment(compliments[randint(0, len(compliments)-1)], media[i]['id'], tag)
                    time.sleep(1)
                b.follow(media[i]['owner']['id'], tag)
                time.sleep(1)
                followed_list.append(media[i]['owner']['id'])
                rand_delay = randint(delay-5,delay+5)/2
                time.sleep(rand_delay)
                if(len(followed_list) > pipe_depth):
                    b.unfollow(followed_list[0])
                    followed_list.pop(0)
                time.sleep(rand_delay)
        except Exception as e:
            print(str(e))
            time.sleep(delay)

    #clean up
    for user in followed_list:
        b.unfollow(user)

def run_cycle(username, password, delay, cycle_length, compliments, hashtags):
    # Create the bot
    b = Bot(username, password)
    time.sleep(2)
    followed_list = []
    #follow people
    while(len(followed_list) < cycle_length):
        try:
            #get the media for a random hashtag
            tag = hashtags[randint(0,len(hashtags)-1)].strip()
            media = b.get_media_from_hashtag(tag)
            #iterate through, like all and comment on a few
            for i in range(len(media)):
                b.like(media[i]['id'])
                time.sleep(1)
                if(randint(0,9) == 0):
                    b.comment(compliments[randint(0, len(compliments)-1)], media[i]['id'], tag)
                    time.sleep(1)
                b.follow(media[i]['owner']['id'])
                time.sleep(1)
                followed_list.append(media[i]['owner']['id'])
                time.sleep(randint(delay-5,delay+5))
                if(len(followed_list) > cycle_length):
                    break
            if(len(followed_list) > cycle_length):
                break
        except Exception as e:
            print(str(e))
            time.sleep(delay)

    #clean up
    clean(username, password, delay, b)

def clean(username, password, delay, b=None): # works for only me!
    if(b==None):
        b = Bot(username, password)
    with open("mcclanewhitelist.txt", "r") as f:
        whitelist = { line.split(" ")[0] : line.split(" ")[1] for line in f.readlines() }
    time.sleep(2)
    follower_count = b.get_follower_count(b.id)
    print("Followers: "+str(follower_count))
    following_count = b.get_following_count(b.id)
    print("Following: "+str(following_count))
    followers_list = b.get_followers(b.id, follower_count)
    following = b.get_following(b.id, following_count)
    followers = {}
    for thing in followers_list:
        followers[thing['node']['id']] = 1

    for thing in following:
        print(thing)
        if not thing['node']['id'] in followers:
            b.unfollow(thing['node']['id'])
            time.sleep(delay)

def WayneWashington(username, password, delay, hashtags, compliments, b=None):
    if(b==None):
        b = Bot(username, password)
    while(True):
        try:
            #get the media for a random hashtag
            tag = hashtags[randint(0,len(hashtags)-1)].strip()
            media = b.get_media_from_hashtag(tag)
            #iterate through, like all and comment on a few
            for i in range(len(media)):
                b.like(media[i]['id'], tag)
                time.sleep(1)
                if(randint(0,9) == 0):
                    b.comment(compliments[randint(0, len(compliments)-1)], media[i]['id'], tag)
                    time.sleep(1)
                time.sleep(randint(delay-5,delay+5))
        except Exception as e:
            print(str(e))
            time.sleep(delay)


def mass_unfollow(username, password, n):
    b = Bot(username, password)
    b.mass_unfollow(n)


if __name__ == '__main__':
    main()
