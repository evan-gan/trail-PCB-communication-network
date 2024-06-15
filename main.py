from machine import Pin, I2C, unique_id
import utime
import math
import _thread

from lib.ssd1306 import SSD1306_I2C
from lib.vcanvas import vCanvas, TextLabel

import radio
import display
# import keyboard
import historyManager

# Turn on the OLED display
Pin(16, Pin.OUT).high()
# Waits for the power to stabilize before initializing the display
utime.sleep(0.5)

ids_seen = []


def receivedMSG(MSG):
    if MSG["ID"] in ids_seen:
        return
    ids_seen.append(MSG["ID"])
    if MSG["TO"] == myname:
        m_historyManager.addMSG(MSG["MSG"])
        # m_display.updateDisplay()
    else:
        m_radio.sendMSG(MSG)


def sendMSG(msg, frm, to):
    msgdict = {
        "MSG": msg,
        "FROM": frm,
        "TO": to,
        "ID": utime.ticks_cpu()
    }
    m_radio.sendMSG(msgdict)


myname = "Board 1"
sendname = "Board 2"

m_radio = radio.Radio(receivedMSG)
m_historyManager = historyManager.HistoryManager()
m_display = display.Display()
# m_keyboard = keyboard.Keyboard(lambda x: m_radio.sendMSG(x, myname, sendname))

m_vcanvas = vCanvas(128, 64, lambda x: m_display.update(x))

labellll = TextLabel(m_vcanvas, {
    "position": {
        "type": "scale",
        "x": 0.5,
        "y": 0.5,
        "ax": 0.5,
        "ay": 0.5
    },
    "text": "Welcome!",
    "textSize": 1,
})

# def calculate_text_position(text, x_center, y_center):
#     char_width = 5
#     char_height = 8
#     text_width = len(text) * char_width
#     text_height = char_height  # Assuming single-line text.

#     top_left_x = int(x_center * 128 - text_width / 2)
#     top_left_y = int(y_center * 64 - text_height / 2)

#     return top_left_x, top_left_y


# i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
# display = SSD1306_I2C(128, 64, i2c, page_addressing=False)

# tlx, tly = calculate_text_position("Welcome!", 0.5, 0.5)
# m_display.display.text("Welcome!", tlx, tly)
# m_display.display.hline(0, 64, 128, 1)
# m_display.display.show()

# tlx, tly = calculate_text_position("Welcome!", 0.5, 0.5)
# tlxx, tlyy = calculate_text_position("Welcome", 0.5, 0.5)

# _thread.start_new_thread(m_vcanvas.thread_function, ("Thread-1", 1))

anogus = 1
while True:
    # utime.sleep(1/60)
    print("Looping", utime.ticks_ms())
    Pin("LED", Pin.OUT).toggle()
    # m_display.test()
    # display.text("Welcome!", tlx, tly, 1)
    # display.show()

    if anogus == 0:
        labellll.text = "Welcome!"
        labellll.x = 1
        labellll.ax = 1
        labellll.y = 1
        labellll.ay = 1
        anogus = 1
    else:
        labellll.text = "Welcome"
        labellll.x = 0.5
        labellll.ax = 0.5
        labellll.y = 0.5
        labellll.ay = 0.5
        anogus = 0

    utime.sleep(1)

    # display.fill(0)

    # display.text("Welcome", tlxx, tlyy, 1)
    # display.show()
    # utime.sleep(1)
    # display.fill(0)


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
