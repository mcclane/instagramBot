import time
import numpy as np
import os
import pandas as pd

class logger_2:
    # TODO: add optional print flag (should print formatted messages)
    # TODO: move follow & unfollow strings to constants in this file
    def __init__(self, username, verbose=True):
        self.username = username
        self.verbose = verbose
        self.base_path = "logs/%s/"%(username.replace(".",""))

        # Set pandas index's for each log
        self.login_log_index = ['time', 'message']
        self.follow_log_index = ['time', 'relationship_change', 'user_id', 'follow_text']
        self.like_log_index = ['time', 'like_change', 'media_id', 'like_text']
        self.comment_log_index = ['time', 'comment_change', 'media_id', 'comment_text']

        # Set base paths for each log
        self.login_log_path = self.base_path + "login_log.pkl"
        self.follow_log_path = self.base_path + "follow_log.pkl"
        self.like_log_path = self.base_path + 'like_log.pkl'
        self.comment_log_path = self.base_path + 'comment_log.pkl'

    def log_login(self, message):
        entry = [time.time(), message]
        self.add_and_save(self.login_log_path, entry, self.login_log_index)

    def log_follow(self, relationship_change, user_id, follow_text):
        entry = [time.time(), relationship_change, user_id, follow_text]
        self.add_and_save(self.follow_log_path, entry, self.follow_log_index)

    def log_like(self, like_change, media_id, like_text):
        entry = [time.time(), like_change, media_id, like_text]
        self.add_and_save(self.like_log_path, entry, self.like_log_index)

    def log_comment(self, comment_change, media_id, comment_text):
        entry = [time.time(), comment_change, media_id, comment_text]
        self.add_and_save(self.comment_log_path, entry, self.comment_log_index)

    def add_and_save(self, path, data, index):
        if self.verbose:
            self.format_print(data, index)
        dataset = load_dataset(path)
        if dataset is None:
            dataset = pd.DataFrame([data], columns=index)
        else:
            dataset = dataset.append(pd.DataFrame([data], columns=index), ignore_index=True)
        save_dataset(path, dataset)

    def format_print(self, data, index):
        # TODO: add formatting for other log types
        if index == self.follow_log_index:
            time = data[0]
            relationship_change = data[1]
            user_id = data[2]
            print("%s: %s at time: %d user: %s"%(self.username, relationship_change, time, user_id))
        else:
            print(data)

def save_dataset(path, data):
    def ensure_dir(file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
    ensure_dir(path)
    data.to_pickle(path)

def load_dataset(path):
    if not os.path.isfile(path):
        return None
    return pd.read_pickle(path)
