from machine import Pin, I2C
import utime, math
import radio, display, keyboard, historyManager

#Stuff to get unique ID
import binascii
import hashlib

#TODO:
    # Move name to history manager - Done
    # Setup name getter system - Done
    # Implement store & Restore into histrory manager and have it call the get name workflow if needed - Done
    # Add json send/receve on lora radio - Package everything into a json?
    # Better font

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
            lambda: self.onEnter(),
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

    def onEnter(self):
        #If full
        if self.historyManager.displayName:
            #The name was defined, so everything can go as normal
            self.sendMessage()
        else:
            self.historyManager.setDisplayName(self.historyManager.getMSG_Draft())
            self.historyManager.clearHistory()
            self.display.update()

    def sendMessage(self):
        msg = self.historyManager.displayName + ":" + self.historyManager.getMSG_Draft()
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
