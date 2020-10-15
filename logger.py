from datetime import datetime, timedelta
import threading
import time
from dataChecker import Checker

class Logger(object):
    """docstring for Logger"""
    def __init__(self):
        super(Logger, self).__init__()
        startTime = datetime.now()
        self.file = "data"
        self.cache = "cache"
        self.workingTime = timedelta(hours=9)
        self.endTime = startTime + self.workingTime
        self.checker = Checker(self.file, self.cache)
        self.state = 'work'
        self.addToFile()
        self.createCacheThread()

    def __del__(self):
        self.state = "stop"
        self.addToFile()

    def addToFile(self):
        with open(self.file, "a") as file:
            file.write(datetime.now().strftime("%c ") + self.state + "\n")
        self.addToCache()


    def getWorkingTime(self):
        return self.workingTime

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        self.addToFile()

    def getLeftTime(self):
        return self.endTime - datetime.now()

    def getLeftTimePercent(self):
        return self.getLeftTime() / self.workingTime

    def getGoneTimePercent(self):
        return (self.workingTime - self.getLeftTime()) / self.workingTime
    
    def createCacheThread(self):
    	self.cacheThread = threading.Thread(target=self.processCache,
    					   daemon=True)
    	self.cacheThread.start()

    def processCache(self):
    	while(True):
    		self.addToCache()
    		time.sleep(5)

    def addToCache(self):
        with open(self.cache, "w") as file:
            file.write(datetime.now().strftime("%c"))