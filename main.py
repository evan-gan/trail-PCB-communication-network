from machine import Pin, unique_id
import uasyncio
import hashlib
import binascii

import datastore
import vcanvas
import display
import keyboard
import typewriter

import ui.greet
import utime

reset = True


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
        display_width, display_height, lambda data: _display.render(data))

    _keyboard = keyboard.Keyboard(lambda key: dummyFunc(key),
                                  lambda: dummyFunc(""),
                                  lambda: dummyFunc(""),
                                  lambda: dummyFunc(""),
                                  lambda: dummyFunc(""),
                                  )

    def dummyFunc(key):
        pass

    # render_task = uasyncio.create_task(_vcanvas.render())

    name = SettingsStore.get("name")

    ui_welcome_screen = vcanvas.Group(_vcanvas)

    ui_welcome_label = vcanvas.TextLabel(ui_welcome_screen, text="", text_size=1, text_color=1,
                                         ax=0, ay=0.5, position_type="scale", x=0.05, y=0.25)

    if name:
        ui_welcome_label_tw = typewriter.Typewriter(
            ui_welcome_label, [
                "Welcome back, ",
                0.5,
                f"{name}!",
            ])

        ui_welcome_label_tw.start()

        await uasyncio.sleep(ui_welcome_label_tw.total_time + 2)
        # utime.sleep(ui_welcome_text_tw.total_time + 2)

        ui_continue_text = vcanvas.TextLabel(ui_welcome_screen, text="Press any key to continue...", text_size=1, text_color=1,
                                             ax=0, ay=0.5, position_type="scale", x=0.05, y=1 - (8/64))

        ui_continue_text.text = "Press any key to continue..."

        await uasyncio.sleep(ui_welcome_label_tw.total_time + 2)
        # utime.sleep(ui_welcome_text_tw.total_time + 2)

        ui.greet.UI_Greet(_vcanvas, False)
    else:
        def saveName(name):
            SettingsStore.add("name", name)

            print("Saved name to database")

            ui_welcome_screen.destroy()

            _keyboard.setFocus(None)

            res = ui.greet.UI_Greet(_vcanvas, True)

            uasyncio.create_task(res.start())

        ui_welcome_label_tw = typewriter.Typewriter(
            ui_welcome_label, [
                "Welcome, ",
                0.5,
                f"user {user_id}!",
            ])

        ui_enter_name_label = vcanvas.TextLabel(ui_welcome_screen, text="", text_size=1, text_color=1,
                                                ax=0, ay=0.5, position_type="scale", x=0.05, y=0.45)

        ui_enter_name_label_tw = typewriter.Typewriter(
            ui_enter_name_label, [
                "Enter your name: "
            ])

        ui_name_box = vcanvas.TextBox(ui_welcome_screen, text="", text_size=1, text_color=1, text_limit=19*3,
                                      ax=0, ay=0.5, position_type="scale", x=0.05, y=0.65, onEnter=lambda self: saveName(self.text))

        ui_welcome_label_tw.start()

        await uasyncio.sleep(ui_welcome_label_tw.total_time + 2)
        # utime.sleep(ui_welcome_text_tw.total_time + 2)

        ui_enter_name_label_tw.start()

        await uasyncio.sleep(ui_enter_name_label_tw.total_time + 3)
        # utime.sleep(ui_enter_name_tw.total_time + 3)

        _keyboard.setFocus(ui_name_box)

        # def update(stuff):
        #     label.text += stuff

        # def dele():
        #     if label.text:
        #         label.text = label.text[:-1]

        # _keyboard = user_input.Keyboard(lambda key: update(key),
        #                               lambda: update("\n"),
        #                               lambda: dele())

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
