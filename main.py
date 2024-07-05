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
        utime.sleep(0.5)


        self.radio = radio.Radio(self.receivedMSG)
        self.historyManager = historyManager.HistoryManager()
        self.display = display.Display(historyManager)
        #NOTE: Should figure out user ID system
        #NOTE: Make sure to use set draft & send for view updates to work
        self.keyboard = keyboard.Keyboard(self.addLetterToDraft, self.sendMessage, self.backspace, self.display.scrollUp, self.display.scrollDown)
        #Lambda format:
            #lambda param : <Any code>

    def run(self):
        #Loop can go here to keep the program running
        while True:
            utime.sleep(1)
            print("Running!")

    #Functions that get passed as lambda's:
    def receivedMSG(self, MSG):
        self.historyManager.addMSG(MSG)
        self.display.update()

    def sendMessage(self):
        self.display.update()

    def backspace(self):
        self.historyManager.deleteLastCharFromDraft()
        self.display.update()

    def addLetterToDraft(self, char):
        self.historyManager.appendToDraft(char)
        self.display.update()











# # Main loop function
# def loop():
#     global scroll  # Declare scroll as global
#     while True:
#         utime.sleep(0.1)
#         # led_pin.toggle()

#         # print(Pin(ROW_GS_PIN, Pin.IN, Pin.PULL_UP).value(), Pin(ROW_PINS[0], Pin.IN, Pin.PULL_UP).value(), Pin(ROW_PINS[1], Pin.IN, Pin.PULL_UP).value(), Pin(ROW_PINS[2], Pin.IN, Pin.PULL_UP).value())

#         # for row in range(3):
#         #     for col in range(3):
#         #         if Pin(COL_PINS[col]).value():
#         #             print(f"Row {row} Col {col} pressed")

#         # scroll += 1
#         # updateDisplay()
#         # sendMSG("Hi!", name)
# # Run the loop function indefinitely

# # history.append("Me: Hi there!")
# # history.append("J101: Hello E404!")
# # history.append("Me: Lets meet at the camp")
# # history.append("J101: Ok, let me walk back over the hill")
    
board = BOARD_MANAGER()
board.run()