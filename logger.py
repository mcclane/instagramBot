import time
class logger:
    def __init__(self, name):
        self.name = name
    def write(self, message):
        f = open(self.name, "a")
        f.write("%d: %s" % (time.time(), message))
        f.close()
