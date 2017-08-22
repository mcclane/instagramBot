from bot import Bot
from getpass import getpass
from random import randint
import time

def run_bot(delay, pipe_depth, number_of_tags, compliments, hashtags):
    print("delay:", delay)

    # Create the bot
    b = Bot(input("USERNAME: "), getpass("PASSWORD: "))
    time.sleep(2)
    followed_list = []
    for i in range(number_of_tags):
        #get the media for a random hashtag
        tag = hashtags[randint(0,len(hashtags)-1)].strip()
        media = b.get_media_from_hashtag(tag)
        #iterate through, like all and comment on a few
        for i in range(len(media)):
            b.like(media[i]['id'])
            time.sleep(1)
            if(i == len(media)/2):
                b.comment(compliments[randint(0, len(compliments)-1)], media[i]['id'])
                time.sleep(1)
            #b.follow(media[i]['owner']['id'])
            time.sleep(1)
            #followed_list.append(media[i]['owner']['id'])
            if(len(followed_list) > pipe_depth):
                b.unfollow(followed_list[0])
                followed_list.pop(0)
            # TODO: should make delay random?
            time.sleep(delay)

    #clean up
    for user in followed_list:
        b.unfollow(user)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument('instruction', type=str)
    parser.add_argument('--hashtag_type', type=str, default='big_list', help='Options: big_list, surfing')
    parser.add_argument('--delay', type=int, default=120)
    parser.add_argument('--pipe_depth', type=int, default=200)
    parser.add_argument('--number_of_tags', type=int, default=1000)
    args = parser.parse_args()

    # Get the resources
    cs = open("resources/compliment_strings.txt", "r")
    compliments = cs.readlines()
    cs.close()

    if args.hashtag_type == 'big_list':
        h = open("resources/hashtags.txt", "r")
    elif args.hashtag_type == 'surfing':
        h = open("resources/surfing_hashtags.txt", "r")
    else:
        raise ValueError('Argument hashtag_type %s invalid.'%args.hashtag_type)

    hashtags = h.readlines()
    h.close()

    print("starting pipeline")
    run_bot(args.delay, args.pipe_depth, args.number_of_tags, compliments, hashtags)

if __name__ == '__main__':
    main()
