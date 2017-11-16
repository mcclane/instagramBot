import logger

def follower_analysis(username):
    logs = logger.logger_2(username)
    follow_data = logger.load_dataset(logs.follow_log_path)

    # User ids that were followed and unfollowed by bot
    terminated_followings = []
    # once logs get big, use dictionary for open_followings to speed up
    # User ids the bot has followed but not yet unfollowed
    open_followings = []
    # User ids that were unfollowed but not followed by bot
    error_unfollows = []
    # Number of times an account was followed more than once
    duplicate_follow_count = 0

    # Iterate over follow_data twice, once to add and one to remove
    print("Getting open_follows")
    i = 0
    for row in follow_data.itertuples():
        i += 1
        if (i%200==0):
            print("open_follows:" + str(i))
        # Hacky way of getting relationship_change and user_id because
        # Pandas indexing not available on rasberry pi
        row_relationship_change = row[2]
        row_user_id = row[3]
        try:
            if row_relationship_change == "follow":
                if row_user_id in open_followings:
                    duplicate_follow_count += 1
                else:
                    open_followings.append(row_user_id)
        except Exception as e:
            print(str(e))

    print("getting terminated followers")
    i = 0
    for row in follow_data.itertuples():
        i += 1
        if (i%200==0):
            print("stage 2:"+str(i))
        row_relationship_change = row[2]
        row_user_id = row[3]
        if row_relationship_change == "unfollow":
            if row_user_id in open_followings:
                open_followings.remove(row_user_id)
                terminated_followings.append(row_user_id)
            else:
                error_unfollows.append(row_user_id)

    analysis = {"terminated_followings" : terminated_followings,
            "open_followings" : open_followings,
            "error_unfollows" : error_unfollows,
            "duplicate_follow_count" : duplicate_follow_count}
    print(analysis)
    return analysis

