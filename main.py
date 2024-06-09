from machine import Pin, I2C

import utime
import math

from ssd1306 import SSD1306_I2C
from sx1262 import SX1262


#The all important name!
myname = "Board 1"
sendname = "Board 2"

TRANSISTOR_PIN = 16
transistor = Pin(TRANSISTOR_PIN, Pin.OUT)
transistor.high()

# for pin in COL_PINS:
#     Pin(pin, Pin.IN, Pin.PULL_UP)

# for pin in ROW_PINS:
#     Pin(pin, Pin.IN, Pin.PULL_UP)

#Settings/constants for OLED display:
CHAR_PER_LINE = 16 #Old was 21, should change font back later
LINES = 6

# idk why but removing this delay breaks the code
utime.sleep(0.5)

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


# Shift key send example message
SHIFT_PIN = Pin(28, Pin.IN, Pin.PULL_UP)

COL_GS_PIN = Pin(7, Pin.IN)
ROW_GS_PIN = Pin(9, Pin.IN, Pin.PULL_UP)

COL_PINS = [10, 27, 6]
ROW_PINS = [14, 13, 21]

# Variable to store the last button press time
last_press_time = 0
last_press_time_d = 0

def shift_pressed(pin):
    global last_press_time
    current_time = utime.ticks_ms()
    # Check if the debounce time (200 ms) has passed
    if utime.ticks_diff(current_time, last_press_time) > 200:
        sendMSG("hello world!", myname, sendname)
        last_press_time = current_time

led_pin = Pin("LED", Pin.OUT)

def keypor(pin):
    global last_press_time_d
    current_time = utime.ticks_ms()
    # Check if the debounce time (200 ms) has passed
    if utime.ticks_diff(current_time, last_press_time_d) > 200:
        print("Key pressed", current_time)
        led_pin.toggle()
        last_press_time_d = current_time

# Set up an interrupt to detect button presses
SHIFT_PIN.irq(trigger=Pin.IRQ_FALLING, handler=shift_pressed)

# COL_GS_PIN.irq(trigger=Pin.IRQ_FALLING, handler=keypor)

Pin(COL_PINS[0], Pin.IN, Pin.PULL_UP).irq(trigger=Pin.IRQ_FALLING, handler=keypor)

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



def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print('Received {}, {}'.format(msg, error))
        if error == "ERR_NONE":
            # if msg[1] == myname: # this line will only work once changing name is implemented
            receivedMSG(str(msg)) # needs to be implemented

    elif events & SX1262.TX_DONE:
        print('done transmitting')
    pass

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)
sx.begin(freq=902.0, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=0, useRegulatorLDO=False, blocking=True)
sx.setBlockingCallback(False, cb)

def sendMSG(msg, frm, to): # from and to
    # sx.send(bytes(f"{frm}|{to}|{msg}", 'utf-8'))
    sx.send(bytes(f"{frm}: {msg}", 'utf-8'))

#
#   General combinding everything together func's
#

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
        utime.sleep(0.1)
        # led_pin.toggle()

        # print(Pin(ROW_GS_PIN, Pin.IN, Pin.PULL_UP).value(), Pin(ROW_PINS[0], Pin.IN, Pin.PULL_UP).value(), Pin(ROW_PINS[1], Pin.IN, Pin.PULL_UP).value(), Pin(ROW_PINS[2], Pin.IN, Pin.PULL_UP).value())

        # for row in range(3):
        #     for col in range(3):
        #         if Pin(COL_PINS[col]).value():
        #             print(f"Row {row} Col {col} pressed")

        # scroll += 1
        # updateDisplay()
        # sendMSG("Hi!", name)
# Run the loop function indefinitely

# history.append("Me: Hi there!")
# history.append("J101: Hello E404!")
# history.append("Me: Lets meet at the camp")
# history.append("J101: Ok, let me walk back over the hill")

updateDisplay()

loop()