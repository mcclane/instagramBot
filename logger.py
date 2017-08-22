import time
import numpy as np
import os
import pandas as pd

class logger:
    def __init__(self, name):
        self.name = name
    def write(self, message):
        f = open(self.name, "a")
        f.write("%d: %s" % (time.time(), message))
        f.close()

class logger_2:
    # TODO: add optional print flag (should print formatted messages)
    # TODO: move follow & unfollow strings to constants in this file
    def __init__(self, username, verbose=True):
        self.username = username
        self.verbose = verbose
        self.base_path = "logs/%s/"%(username.replace(".",""))

        self.login_log_index = ['time', 'message']
        self.login_log_path = self.base_path + "login_log.pkl"

        self.follow_log_index = ['time', 'relationship_change', 'user_id', 'follow_text']
        self.follow_log_path = self.base_path + "follow_log.pkl"

    def log_login(self, message):
        entry = [time.time(), message]
        self.add_and_save(self.login_log_path, entry, self.login_log_index)

    def log_follow(self, relationship_change, user_id, follow_text):
        entry = [time.time(), relationship_change, user_id, follow_text]
        self.add_and_save(self.follow_log_path, entry, self.follow_log_index)

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
        if index == self.follow_log_index:
            time = data[0]
            relationship_change = data[1]
            print("%s at time: %d"%(relationship_change, time))
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
