from machine import Pin, I2C, unique_id
import utime
import math

from lib.ssd1306 import SSD1306_I2C

import radio
import display
import keyboard
import historyManager

# Turn on the OLED display
Pin(16, Pin.OUT).high()
# Waits for the power to stabilize before initializing the display
utime.sleep(0.5)


def receivedMSG(historyManager, MSG):
    global history
    m_historyManager.addMSG(MSG)
    # m_display.updateDisplay()


myname = "Board 1"
sendname = "Board 2"

m_radio = radio.Radio(lambda x: receivedMSG(m_historyManager, x))
m_historyManager = historyManager.HistoryManager()
# m_display = display.Display(m_historyManager)
m_keyboard = keyboard.Keyboard(lambda x: m_radio.sendMSG(x, myname, sendname))


def calculate_text_position(text, x_center, y_center):
    char_width = 5
    char_height = 8
    text_width = len(text) * char_width
    text_height = char_height  # Assuming single-line text.

    top_left_x = int(x_center * 128 - text_width / 2)
    top_left_y = int(y_center * 64 - text_height / 2)

    return top_left_x, top_left_y


i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
display = SSD1306_I2C(128, 64, i2c, page_addressing=False)

# tlx, tly = calculate_text_position("Welcome!", 0.5, 0.5)
# m_display.display.text("Welcome!", tlx, tly)
# m_display.display.hline(0, 64, 128, 1)
# m_display.display.show()

tlx, tly = calculate_text_position("Welcome!", 0.5, 0.5)
tlxx, tlyy = calculate_text_position("Welcome", 0.5, 0.5)

while True:
    # utime.sleep(1/60)
    print("Looping", utime.ticks_ms())
    Pin("LED", Pin.OUT).toggle()
    display.text("Welcome!", tlx, tly, 1, size=1)
    display.show()
    utime.sleep(1)
    display.fill(0)

    display.text("Welcome", tlxx, tlyy, 1, size=1)
    display.show()
    utime.sleep(1)
    display.fill(0)


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
