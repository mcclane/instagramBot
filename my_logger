from logging import *
import sys

#set up the logger
#configure filename, level, and message format
basicConfig(filename='general.log', level=INFO, format='%(asctime)s %(message)s') #timestamp, message
#instantiate a root logger object 
logger = getLogger()
#create an stdout logger to print the messages 
output = StreamHandler(sys.stdout)
#set level for output (same as root logger)
output.setLevel(INFO)
#set format for output logger
formatter = Formatter('%(asctime)s %(message)s')
output.setFormatter(formatter)
#add the output to the root logger
logger.addHandler(output) #now log messages will also be printed to the terminal

def log_message(level, message):
    if(level == "debug"):
        logger.debug(message)
    elif(level == "info"):
        logger.info(message)
    elif(level == "warn"):
        logger.warn(message)
    elif(level == "error"):
        logger.error(message)
    else:
        logger.info(message)
    

