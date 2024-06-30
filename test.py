from machine import Pin, unique_id
import uasyncio
import hashlib
import binascii

import datastore
import vcanvas
import display
import keyboard
import typewriter


async def main():
    # Turn on the OLED display
    Pin(16, Pin.OUT).high()
    # Waits for the power to stabilize before initializing the display
    await uasyncio.sleep(0.5)

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

    ui_welcome_text = vcanvas.TextLabel(_vcanvas, text="", text_size=1, text_color=1,
                                        ax=0, ay=0.5, position_type="scale", x=0.1, y=0.25)

    ui_welcome_text_tw = typewriter.Typewriter(
        ui_welcome_text, [
            "Welcome, ",
            0.5,
            f"user {user_id}!",
        ])

    ui_welcome_text_tw.start()

    await uasyncio.sleep(ui_welcome_text_tw.total_time + 2)

    ui_enter_name = vcanvas.TextLabel(_vcanvas, text="", text_size=1, text_color=1,
                                      ax=0, ay=0.5, position_type="scale", x=0.1, y=0.45)

    ui_enter_name_tw = typewriter.Typewriter(
        ui_enter_name, [
            "Enter your name: "
        ])

    ui_enter_name_tw.start()

    await uasyncio.sleep(ui_enter_name_tw.total_time + 2)

    ui_name_box = vcanvas.TextBox(_vcanvas, text="", text_size=1, text_color=1,
                                  ax=0, ay=0.5, position_type="scale", x=0.1, y=0.55)

    ui_name_box.focus()

    # def update(stuff):
    #     label.text += stuff

    # def dele():
    #     if label.text:
    #         label.text = label.text[:-1]

    _keyboard = keyboard.Keyboard(lambda key: update(key),
                                  lambda: update("\n"),
                                  lambda: dele())

    amogus = 0

    while True:
        await uasyncio.sleep(1)

        # print("Looping", utime.ticks_ms())
        Pin("LED", Pin.OUT).toggle()

        if amogus == 0:
            amogus = 1
        elif amogus == 1:

            amogus = 0

        # await uasyncio.sleep(2)

uasyncio.run(main())
