from lib.ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import utime
import math
import CONSTS
from historyManager import HistoryManager
#
#   UTILITY FOR PRINTING TO DISPLAY
#
class Display:
    #Scroll stores the line that is being viewed (aka the line that is at the top)

    def __init__(self, historyManager):
        utime.sleep(0.5)
        self.historyManager:HistoryManager = historyManager
        #Display initilisation
        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        self.display = SSD1306_I2C(128, 64, self.i2c, addr=0x3c)

        self.scroll = 0

    def linesForMessage(self,MSG):
        MESSAGE_LENGTH:int = len(MSG)
        # print(MSG_Draft)
        return math.ceil(MESSAGE_LENGTH/CONSTS.CHAR_PER_LINE)

    #Splits a message into lines
    def splitMessageIntoLines(self,MSG) -> list[str]:
        splitMSG = []
        linesInMSG = self.linesForMessage(MSG)
        for line in range(linesInMSG-1):
            splitMSG.append(MSG[line*CONSTS.CHAR_PER_LINE:(line+1)*CONSTS.CHAR_PER_LINE]) #Gets the line's chunk
        splitMSG.append(MSG[(linesInMSG-1)*CONSTS.CHAR_PER_LINE:])
        return splitMSG

    #Gets all messages (including the draft) as a format that could be printed
    def getLatestMessagesAsLines(self) -> list[str]:
        lineBroken:list[str] = self.splitMessageIntoLines(self.historyManager.getMSG_Draft())
        for text in reversed(self.historyManager.getHistory()):
            lineBroken += self.splitMessageIntoLines(text)
        return lineBroken

    def scrollUp(self):
        self.scroll += 1
        self.update()

    def scrollDown(self):
        if (self.scroll > 0):
            self.scroll -= 1
            self.update()
#
#   Display interactions:
#
    def writeToLine(self,line, text):
        LINE_OFFSET = CONSTS.CHAR_HEIGHT + 1
        self.display.text(text, 0, LINE_OFFSET*line)

    def clearDisplay(self):
        self.display.fill(0)

    def showDisplay(self):
        self.display.show()

    #TODO: Double check scroll limiting
    def update(self):
        self.clearDisplay()
        stuffToDisplay = self.getLatestMessagesAsLines()
        length = len(stuffToDisplay)
        index = 0
        while ((index+self.scroll) < length and index < self.scroll+CONSTS.LINES and self.scroll >= 0):
            self.writeToLine(index, stuffToDisplay[index+self.scroll])
            index += 1
        self.showDisplay()

    #Debugging help:
    def scan_i2c(self):
        devices = self.i2c.scan()
        if devices:
            print("I2C devices found:", [hex(device) for device in devices])
        else:
            print("No I2C devices found")