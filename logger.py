from datetime import datetime, timedelta


class Logger(object):
    """docstring for Logger"""
    def __init__(self):
        super(Logger, self).__init__()
        startTime = datetime.now()
        self.workingTime = timedelta(hours=9)
        self.endTime = startTime + self.workingTime
        self.state = 'work'
        self.addToFile()

    def __del__(self):
        self.state = "stop"
        self.addToFile()

    def addToFile(self):
        with open("data", "a") as file:
            file.write(datetime.now().strftime("%c ") + self.state + "\n")

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
