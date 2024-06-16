from machine import Pin, I2C, unique_id
import utime
import math
# import _thread
import uasyncio

from lib.ssd1306 import SSD1306_I2C

import vcanvas
import radio
from display import Display
# import keyboard
import historyManager

# Stops all running threads apart from main
stop_requested = False

# Turn on the OLED display
Pin(16, Pin.OUT).high()
# Waits for the power to stabilize before initializing the display
utime.sleep(0.5)

# ids_seen = []


# def receivedMSG(MSG):
#     if MSG["ID"] in ids_seen:
#         return
#     ids_seen.append(MSG["ID"])
#     if MSG["TO"] == myname:
#         m_historyManager.addMSG(MSG["MSG"])
#         # m_display.updateDisplay()
#     else:
#         m_radio.sendMSG(MSG)


# def sendMSG(msg, frm, to):
#     msgdict = {
#         "MSG": msg,
#         "FROM": frm,
#         "TO": to,
#         "ID": utime.ticks_cpu()
#     }
#     m_radio.sendMSG(msgdict)


# myname = "Board 1"
# sendname = "Board 2"

# m_radio = radio.Radio(receivedMSG)
# m_historyManager = historyManager.HistoryManager()

# anogus = 1
# while True:
#     # utime.sleep(1/60)
#     print("Looping", utime.ticks_ms())
#     Pin("LED", Pin.OUT).toggle()
#     # m_display.test()
#     # display.text("Welcome!", tlx, tly, 1)
#     # display.show()

#     if anogus == 0:
#         labellll.text = "Welcome!"

#         labellll.position_type = "scale"

#         labellll.x = 1
#         labellll.y = 1

#         labellll.ax = 1
#         labellll.ay = 1

#         anogus = 1
#     else:
#         labellll.text = "Happy"

#         labellll.position_type = "offset"

#         labellll.x = 64
#         labellll.y = 32

#         labellll.ax = 0.5
#         labellll.ay = 0.5

#         anogus = 0

#     utime.sleep(1)

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

async def main():
    _display = Display()
    _vcanvas = vcanvas.vCanvas(128, 64, lambda data: _display.render(data))

    render_task = uasyncio.create_task(_vcanvas.render())

    frame = vcanvas.Frame(_vcanvas, width=64, height=32, fill=True,
                          ax=0.5, ay=0.5, position_type="scale", x=0.5, y=0.5)

    label = vcanvas.TextLabel(frame, text="Welcome!", text_size=1, text_color=0,
                              ax=0.5, ay=0.5, position_type="scale", x=0.5, y=0.5)

    sframe = vcanvas.Frame(frame, size_type="scale", width=0.5, height=1, fill=True,
                           ax=0, ay=0.5, position_type="scale", x=0, y=0.5)

    amogus = 1

    try:
        while True:
            await uasyncio.sleep(1)

            print("Looping", utime.ticks_ms())
            Pin("LED", Pin.OUT).toggle()

            if amogus == 0:
                frame.x = 0.25
                frame.y = 0.25
                label.text = "Welcome!"
                amogus = 1
            elif amogus == 1:
                frame.x = 0.75
                frame.y = 0.75
                label.text = "Welcome"
                amogus = 0
    finally:
        render_task.cancel()

        try:
            await render_task
        except uasyncio.CancelledError:
            print("Cancelled render task")

uasyncio.run(main())
