from machine import Pin, unique_id
import uasyncio
import hashlib
import binascii

import datastore
import vcanvas
import typewriter
import display
import keyboard
import radio

import ui.greet
import utime

reset = False


async def main():
    # Turn on the OLED display
    Pin(16, Pin.OUT).high()
    # Waits for the power to stabilize before initializing the display
    await uasyncio.sleep(0.5)
    # utime.sleep(0.5)

    SettingsStore = datastore.DataStore("settings")

    if reset:
        SettingsStore.clear()

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
        display_width, display_height, _display.render)

    _keyboard = keyboard.Keyboard(lambda key: dummyFunc(key),
                                  lambda: dummyFunc(""),
                                  lambda: dummyFunc(""),
                                  lambda: dummyFunc(""),
                                  lambda: dummyFunc(""),
                                  )

    # _radio = radio.Radio()

    def dummyFunc(key):
        pass

    # render_task = uasyncio.create_task(_vcanvas.render())

    name = SettingsStore.get("name")

    ui_welcome_screen = vcanvas.Group(_vcanvas)

    ui_welcome_label = vcanvas.TextLabel(ui_welcome_screen, text="", text_size=1, text_color=1,
                                         ax=0, ay=0.5, position_type="scale", x=0.05, y=0.2)

    if name:
        def homePage():
            ui_welcome_screen.destroy()

        ui_welcome_label_tw = typewriter.Typewriter(
            ui_welcome_label, [
                "Welcome back, ",
                0.5,
                f"{name}!",
            ])

        ui_welcome_label_tw.start()

        await uasyncio.sleep(ui_welcome_label_tw.total_time + 2)

        ui_continue_text = vcanvas.TextLabel(ui_welcome_screen, text="Press any key to continue...", text_size=1, text_color=1,
                                             ax=0, ay=0.5, position_type="scale", x=0.05, y=1 - (8/64))

        ui_continue_text.text = "Press any key to continue..."

        _keyboard.onceKeyPress("", homePage)
    else:
        def saveName(self):
            SettingsStore.add("name", self.text)

            print("Saved name to database")

            ui_welcome_screen.destroy()

            _keyboard.setFocus(None)

            ui_greet = ui.greet.UI_Greet(_vcanvas, self.text)

            uasyncio.create_task(ui_greet.start())

        ui_welcome_label_tw = typewriter.Typewriter(
            ui_welcome_label, [
                "Welcome, ",
                0.5,
                f"user {user_id}!",
            ])

        ui_enter_name_label = vcanvas.TextLabel(ui_welcome_screen, text="", text_size=1, text_color=1,
                                                ax=0, ay=0.5, position_type="scale", x=0.05, y=0.4)

        ui_enter_name_label_tw = typewriter.Typewriter(
            ui_enter_name_label, [
                "Enter your name: "
            ])

        ui_name_box = vcanvas.TextBox(ui_welcome_screen, text="", text_size=1, text_color=1, text_limit=19*3,
                                      ax=0, ay=0.5, position_type="scale", x=0.05, y=0.6, onEnter=saveName)

        ui_welcome_label_tw.start()

        await uasyncio.sleep(ui_welcome_label_tw.total_time + 2)

        ui_enter_name_label_tw.start()

        await uasyncio.sleep(ui_enter_name_label_tw.total_time + 3)

        _keyboard.setFocus(ui_name_box)

        amogus = 0

        while True:
            await uasyncio.sleep(1)
            # utime.sleep(1)

            # print("Looping", utime.ticks_ms())
            Pin("LED", Pin.OUT).toggle()

            if amogus == 0:
                amogus = 1
            elif amogus == 1:

                amogus = 0

        # await uasyncio.sleep(2)


uasyncio.run(main())
