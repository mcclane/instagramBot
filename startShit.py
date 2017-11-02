import subprocess
import sys

with open("users.txt", "r") as f:
    for line in f.readlines():
        username, password = line.split(",")
        subprocess.Popen(["nohup", "python3", "controller.py", "--username", username, "--password ", password])
        print("Started "+username)
