from machine import Pin, I2C
from lib.ssd1306 import SSD1306_I2C
import utime
import math
#LoRa Lib
from lib.sx1262 import SX1262


TRANSISTOR_PIN = 16
transistor = Pin(TRANSISTOR_PIN, Pin.OUT)

transistor.high()

#Settings/constants for OLED display:
CHAR_PER_LINE = 16 #Old was 21, should change font back later
LINES = 6

#Where the messages & draft are stored
history:list[str] = []
MSG_Draft:str = "Me: How long will that take?"
#Scroll stores the line that is being viewed (aka the line that is at the top)
scroll = 0

# Define the screen dimensions
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# Define the I2C pins
OLED_SDA = 0
OLED_SCL = 1

# Initialize I2C
i2c = I2C(0, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)

# Create an SSD1306 display object
display = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c, addr=0x3c)

#
#   UTILITY FOR PRINTING TO DISPLAY
#

#Finds the amount of lines needed for message to display
def linesForMessage(MSG):
    MESSAGE_LENGTH:int = len(MSG)
    # print(MSG_Draft)
    return math.ceil(MESSAGE_LENGTH/CHAR_PER_LINE)

#Splits a message into lines
def splitMessageIntoLines(MSG) -> list[str]:
    splitMSG = []
    linesInMSG = linesForMessage(MSG)
    for line in range(linesInMSG-1):
        splitMSG.append(MSG[line*CHAR_PER_LINE:(line+1)*CHAR_PER_LINE]) #Gets the line's chunk
    splitMSG.append(MSG[(linesInMSG-1)*CHAR_PER_LINE:])
    return splitMSG

#Gets all messages (including the draft) as a format that could be printed
def getLatestMessagesAsLines() -> list[str]:
    lineBroken:list[str] = splitMessageIntoLines(MSG_Draft)
    for text in reversed(history):
        lineBroken += splitMessageIntoLines(text)
    return lineBroken

#Display interactions:
def writeToLine(line, text):
    LINE_OFFSET = 10
    display.text(text, 0, LINE_OFFSET*line)

def clearDisplay():
    display.fill(0)

def showDisplay():
    display.show()

def updateDisplay():
    clearDisplay()
    stuffToDisplay = getLatestMessagesAsLines()
    length = len(stuffToDisplay)
    index = 0
    while ((index+scroll) < length and index < scroll+LINES):
        writeToLine(index, stuffToDisplay[index+scroll])
        index += 1
    showDisplay()

def receivedMSG(MSG):
    global history
    history.append(MSG)
    updateDisplay()

#
#   LoRa stuff
#

name = "D1"

def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print('Received {}, {}'.format(msg, error))
        if error == "ERR_NONE":
            # if str(msg).split("|")[0] == name:
                # recivedMSG(str(msg).split("|")[1]) # needs to be implemented
            recivedMSG(str(msg)) # needs to be implemented

    elif events & SX1262.TX_DONE:
        print('done transmitting')
    pass

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)
sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
sx.setBlockingCallback(False, cb)

def sendMSG(msg, recp):
    sx.send(bytes(recp + "|" + msg))

#
#   General combinding everything together func's
#

def recivedMSG(MSG):
    global history #Import history for local use
    history.append(MSG)
    updateDisplay()
    print("Updated! The msg was:"+MSG)

# Function to scan I2C devices
def scan_i2c():
    devices = i2c.scan()
    if devices:
        print("I2C devices found:", [hex(device) for device in devices])
    else:
        print("No I2C devices found")

# Main loop function
def loop():
    global scroll  # Declare scroll as global
    while True:
        utime.sleep(1)
        # scroll += 1
        # updateDisplay()
        sendMSG("Hi!",name)
# Run the loop function indefinitely

history.append("Me: Hi there!")
history.append("J101: Hello E404!")
history.append("Me: Lets meet at the camp")
history.append("J101: Ok, let me walk back over the hill")

updateDisplay()

loop()
