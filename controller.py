from bot import Bot
from getpass import getpass
from random import randint
import time

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
'''
def main():
    import argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument('instruction', type=str)
    parser.add_argument('--hashtag_type', type=str, default='big_list', help='Options: big_list, surfing, travel')
    parser.add_argument('--delay', type=int, default=120)
    parser.add_argument('--pipe_depth', type=int, default=200)
    parser.add_argument('--number_of_tags', type=int, default=1000)
    parser.add_argument('--cycle', type=int, default=None)
    parser.add_argument('--username', type=str, default=None)
    parser.add_argument('--password', type=str, default=None)
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
    else:
        raise ValueError('Argument hashtag_type %s invalid.'%args.hashtag_type)

    hashtags = h.readlines()
    h.close()

    if(args.cycle != None):
        print("starting cycle")
        run_cycle(username, password, args.delay, args.cycle, compliments, hashtags)
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
                #b.like(media[i]['id'])
                time.sleep(1)
                if(i == len(media)/2):
                    b.comment(compliments[randint(0, len(compliments)-1)], media[i]['id'])
                    time.sleep(1)
                b.follow(media[i]['owner']['id'])
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
    for i in range(cycle_length):
        try:
            #get the media for a random hashtag
            tag = hashtags[randint(0,len(hashtags)-1)].strip()
            media = b.get_media_from_hashtag(tag)
            #iterate through, like all and comment on a few
            for i in range(len(media)):
                #b.like(media[i]['id'])
                time.sleep(1)
                if(i == len(media)/2):
                    b.comment(compliments[randint(0, len(compliments)-1)], media[i]['id'])
                    time.sleep(1)
                b.follow(media[i]['owner']['id'])
                time.sleep(1)
                followed_list.append(media[i]['owner']['id'])
                time.sleep(randint(delay-5,delay+5))
        except Exception as e:
            print(str(e))
            time.sleep(delay)

    #clean up
    for user in followed_list:
        try:
            b.unfollow(user)
            time.sleep(randint(delay-5, delay+5))
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    main()
