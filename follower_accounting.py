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
    for row in follow_data.itertuples():
        if row.relationship_change == "follow":
            if row.user_id in open_followings:
                duplicate_follow_count += 1
            else:
                open_followings.append(row.user_id)

    for row in follow_data.itertuples():
        if row.relationship_change == "unfollow":
            if row.user_id in open_followings:
                open_followings.remove(row.user_id)
                terminated_followings.append(row.user_id)
            else:
                error_unfollows.append(row.user_id)

    return {"terminated_followings" : terminated_followings,
            "open_followings" : open_followings,
            "error_unfollows" : error_unfollows,
            "duplicate_follow_count" : duplicate_follow_count}
