from machine import Pin, I2C
import utime, math
import radio, display, keyboard, historyManager

#Stuff to get unique ID
import binascii
import hashlib


# user_id = user_id = binascii.hexlify(hashlib.sha1(
#             unique_id()).digest()).decode("utf-8")[:4]

myname = "Board 1"

class BOARD_MANAGER:
    def __init__(self):
        #INIT DISPLAY
        TRANSISTOR_PIN = 16
        transistor = Pin(TRANSISTOR_PIN, Pin.OUT)
        transistor.high()
        # utime.sleep(0.5)


        self.radio = radio.Radio(self.receivedMSG)
        self.historyManager = historyManager.HistoryManager()
        self.display = display.Display(self.historyManager)
        #NOTE: Should figure out user ID system
        #NOTE: Make sure to use set draft & send for view updates to work
        self.keyboard = keyboard.Keyboard(
            lambda x: self.addLetterToDraft(x),
            lambda: self.sendMessage(),
            lambda: self.backspace(),
            lambda: self.display.scrollUp(),
            lambda: self.display.scrollDown()
        )

        self.display.update()
        #Lambda format:
            #lambda param : <Any code>

    def run(self):
        #Loop can go here to keep the program running
        while True:
            utime.sleep(1)
            # print("Running!")

    #Functions that get passed as lambda's:
    def receivedMSG(self, MSG):
        self.historyManager.addMSG(MSG)
        self.display.update()

    def sendMessage(self):
        msg = myname + ":" + self.historyManager.getMSG_Draft()
        self.radio.sendMSG(msg)
        self.historyManager.addMSG(msg)
        self.historyManager.setMSG_Draft("")
        self.display.update()

    def backspace(self):
        self.historyManager.deleteLastCharFromDraft()
        self.display.update()

    def addLetterToDraft(self, char):
        self.historyManager.appendToDraft(char)
        self.display.update()

board = BOARD_MANAGER()
board.run()
