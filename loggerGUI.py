import tkinter as tk
import tkinter.ttk as ttk
import time
import threading
from logger import Logger
from tooltip import CreateToolTip
import json


class LoggerGUI(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        self.buttonsInRow = 10
        self.itemWidth = 15
        self.itemHeight = 15
        self.images = []
        self.setStyle()
        self.pack()

        self.logger = Logger()

        self.numButtons = 0
        self.createLabeledProgressBar()
        self.addStateButtons()
        self.addExitButton()
        self.addMenuButton()

    def setStyle(self):
        self.configureWindow()
        self.s = ttk.Style(self)
        self.master.option_add('*Radiobutton*selectColor', "black")
        self.s.layout("LabeledProgressbar",
                      [('LabeledProgressbar.trough',
                        {'children': [('LabeledProgressbar.pbar',
                                       {'side': 'left', 'sticky': 'ns'}),
                                      ("LabeledProgressbar.label",
                                       {"sticky": ""})],
                         'sticky': 'nswe'})])
        self.s.configure("LabeledProgressbar", background='cornflowerblue')

    def configureWindow(self):
        self.master.wm_attributes('-type', 'splash')
        self.master.wm_attributes("-topmost", "true")
        self.master.geometry("+0+0")
        self.master.option_add('*borderWidth', 0)

    def createLabeledProgressBar(self):
        self.pb = ttk.Progressbar(self, orient="horizontal",
                                  length=self.buttonsInRow * self.itemWidth,
                                  maximum=self.buttonsInRow * self.itemWidth,
                                  style="LabeledProgressbar")
        self.pb.grid(row=0, column=0, columnspan=self.buttonsInRow)
        self.pb.isWorkingFlag = True
        self.pb.controlThread = threading.Thread(target=self.progress,
                                                 daemon=True)
        self.pb.controlThread.start()

    def progress(self):
        while(self.pb.isWorkingFlag):
            timePercent = self.logger.getGoneTimePercent()
            self.pb["value"] = timePercent * self.pb["maximum"]
            text = self.timeDeltaToString(self.logger.getLeftTime())
            self.s.configure("LabeledProgressbar",
                             text=text)
            self.update()
            time.sleep(0.04)
        print(timePercent)

    def timeDeltaToString(self, t):
        hours = t.seconds // 3600
        minutes = (t.seconds % 3600) // 60
        seconds = (t.seconds % 3600) % 60
        if self.microsecondsOn:
            microseconds = t.microseconds // 1000
            if microseconds < 100:
                microseconds = "0" + str(microseconds)
                if len(microseconds) < 3:
                    microseconds = "0" + microseconds
            return f"{hours}:{minutes}:{seconds}.{microseconds}       "
        else:
            return f"{hours}:{minutes}:{seconds}       "

    def addStateButtons(self):
        listOfButtons = json.load(open("icons/description"))
        self.radioButtonsState = tk.StringVar()
        self.radioButtonsState.set(self.logger.getState())
        for i, obj in enumerate(listOfButtons):
            image = tk.PhotoImage(file=obj['image'],
                                  width=self.itemWidth,
                                  height=self.itemHeight)
            self.images.append(image)
            button = tk.Radiobutton(self,
                                    variable=self.radioButtonsState,
                                    value=obj['name'],
                                    command=self.stateChanged,
                                    image=image,
                                    indicatoron=False,
                                    )
            CreateToolTip(button, obj["name"])
            button.grid(row=int(self.numButtons / self.buttonsInRow) + 1,
                        column=self.numButtons % self.buttonsInRow,
                        columnspan=1)
            self.numButtons += 1

    def stateChanged(self):
        self.logger.setState(self.radioButtonsState.get())

    def addExitButton(self):
        image = tk.PhotoImage(file="icons/quit.ppm",
                              width=self.itemWidth,
                              height=self.itemHeight)
        self.images.append(image)
        self.b = tk.Button(self,
                           command=self.exit,
                           highlightthickness=0,
                           border=0,
                           image=image,
                           width=self.itemWidth,
                           height=self.itemHeight,
                           )
        CreateToolTip(self.b, "exit")
        self.b.grid(row=int(self.numButtons / self.buttonsInRow) + 1,
                    column=self.numButtons % self.buttonsInRow,
                    columnspan=1)
        self.numButtons += 1

    def exit(self):
        self.logger.setState("stop")
        self.master.destroy()


    def addMenuButton(self):
        self.createMenu()
        image = tk.PhotoImage(file="icons/rat.ppm",
                              width=self.itemWidth,
                              height=self.itemHeight)
        self.images.append(image)
        self.menuButton = tk.Button(self,
                              command=self.showMenu,
                              highlightthickness=0,
                              border=0,
                              image=image,
                              width=self.itemWidth,
                              height=self.itemHeight,
                              )
        CreateToolTip(self.menuButton, "menu")
        self.menuButton.grid(row=int(self.numButtons / self.buttonsInRow) + 1,
                       column=self.numButtons % self.buttonsInRow,
                       columnspan=1)
        self.numButtons += 1

    def createMenu(self):
        self.menu = tk.Menu(tearoff=0)
        self.microsecondsOn = False
        self.menu.add_command(label="Switch microseconds view", command=self.onOffMicroseconds)

    def showMenu(self):
        self.menu.post(self.menuButton.winfo_rootx() + self.menuButton.winfo_width(),
                       self.menuButton.winfo_rooty() + self.menuButton.winfo_height())

    def onOffMicroseconds(self):
        self.microsecondsOn = not self.microsecondsOn


if __name__ == "__main__":
    root = tk.Tk()
    app = LoggerGUI(master=root)
    app.mainloop()
