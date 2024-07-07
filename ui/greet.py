import uasyncio

import vcanvas
import typewriter


class UI_Greet:
    def __init__(self, _vcanvas, first_time):
        self._vcanvas = _vcanvas
        self.first_time = first_time

    async def start(self):
        ui_greeting_screen = vcanvas.Group(self._vcanvas)

        ui_greeting_label = vcanvas.TextLabel(ui_greeting_screen, text="", text_size=1, text_color=1,
                                              ax=0, ay=0.5, position_type="scale", x=0.05, y=0.25)

        ui_greeting_label_tw = typewriter.Typewriter(
            ui_greeting_label, [
                # Extra space so the name wrap to the second line
                "Nice to meet you,  " if self.first_time else "Welcome back, ",
                0.5,
                f"{self.name}!",
            ])

        ui_greeting_label_tw.start()

        await uasyncio.sleep(ui_greeting_label_tw.total_time + 2)
