from machine import Pin, I2C, unique_id
import utime
import math
import uasyncio
import hashlib
import binascii

import datastore
import vcanvas
import display

# Turn on the OLED display
Pin(16, Pin.OUT).high()
# Waits for the power to stabilize before initializing the display
utime.sleep(0.5)


async def main():
    SettingsStore = datastore.DataStore("settings")

    user_id = SettingsStore.get("user_id")

    if user_id:
        print("Loaded user ID from database")
    else:
        print("First-time user, generating unique user ID")

        user_id = binascii.hexlify(hashlib.sha1(
            unique_id()).digest()).decode("utf-8")[:4]

        SettingsStore.add("user_id", user_id)

    display_width, display_height = 128, 64

    _display = display.Display(display_width, display_height)
    _vcanvas = vcanvas.vCanvas(
        display_width, display_height, lambda data: _display.render(data))

    render_task = uasyncio.create_task(_vcanvas.render())

    frame = vcanvas.Frame(_vcanvas, width=64, height=32, fill=False,
                          ax=0.5, ay=0.5, position_type="scale", x=0.5, y=0.5)

    label = vcanvas.TextLabel(frame, text="Welcome!", text_size=1, text_color=1,
                              ax=0.5, ay=0.5, position_type="scale", x=0.5, y=0.5)

    lol = vcanvas.TextLabel(_vcanvas, text=f"{user_id}", text_size=1, text_color=1,
                            ax=0.5, ay=0.5, position_type="scale", x=0.25, y=0.25)

    amogus = 1

    try:
        while True:
            await uasyncio.sleep(1)

            print("Looping", utime.ticks_ms())
            Pin("LED", Pin.OUT).toggle()

            if amogus == 0:
                # frame.x = 0.25
                # frame.y = 0.25
                frame.visible = True
                lol.visible = False
                # label.text = "Welcome!"
                amogus = 1
            elif amogus == 1:
                # frame.x = 0.75
                # frame.y = 0.75
                frame.visible = False
                lol.visible = True
                # label.text = "Welcome"
                amogus = 0
    finally:
        render_task.cancel()

        try:
            await render_task
        except uasyncio.CancelledError:
            print("Cancelled render task")

uasyncio.run(main())
