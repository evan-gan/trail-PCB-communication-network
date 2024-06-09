from machine import Pin, I2C
import utime, math
import radio, display, keyboard, historyManager

TRANSISTOR_PIN = 16
transistor = Pin(TRANSISTOR_PIN, Pin.OUT)
transistor.high()
utime.sleep(0.5)

def receivedMSG(historyManager, MSG):
    global history
    m_historyManager.addMSG(MSG)
    m_display.updateDisplay()

myname = "Board 1"
sendname = "Board 2"

m_radio = radio.Radio(lambda x : receivedMSG(m_historyManager, x))
m_historyManager = historyManager.HistoryManager()
m_display = display.Display(m_historyManager)
m_keyboard = keyboard.Keyboard(lambda x : m_radio.sendMSG(x, myname, sendname))




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