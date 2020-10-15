class Checker(object):
    """docstring for Logger"""
    def __init__(self, file, cache):
        super(Checker, self).__init__()
        self.file = file
        self.cache = cache
        if not self.checkFileStoped():
            self.stopPreviousFile()


    def checkFileStoped(self):
        try:
            with open(self.file, "r") as file:
                line = file.read().splitlines()[-1].split()[-1]
                return line == "stop"
        except Exception as e:
            return True
        

    def stopPreviousFile(self):
        try:
            with open(self.cache, "r") as file:
                line = file.read().splitlines()[-1].split()
                line = " ".join(line)
                with open(self.file, "a") as f:
                    f.write(" ".join((line, "stop\n")))
        except Exception as e:
            file = open(self.file, "r")
            line = file.read().splitlines()[-1].split()[:-1]
            line = " ".join(line)
            file.close()
            with open(self.file, "a") as f:
                f.write(" ".join((line, "stop\n")))
