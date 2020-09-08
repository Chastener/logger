from datetime import datetime


class Reporter(object):
    """docstring for Reporter"""

    def __init__(self):
        super(Reporter, self).__init__()
        self.times = {}
        self.readData()
        print(self)

    def readData(self):
        with open("data", "r") as file:
            lines = file.readlines()
        prevTime, state = self.getTimeStateFromLine(lines[0])
        for line in lines[1:]:
            time, nextState = self.getTimeStateFromLine(line)
            if(self.times.__contains__(state)):
                self.times[state] += time - prevTime
            else:
                self.times[state] = time - prevTime
            state = nextState
            prevTime = time
        self.times.pop('stop')

    def getTimeStateFromLine(self, line):
        state = line.split()[-1]
        length = len(state)
        line = line[:-length - 1]
        time = datetime.strptime(line, "%c\n")
        return time, state

    def __repr__(self):
        string = ""
        for key in self.times:
            string += key + ": " + str(self.times[key]) + "\n"
        return string


if __name__ == "__main__":
    r = Reporter()
