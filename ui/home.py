import uasyncio

import vcanvas


class UI_Home:
    def __init__(self, _vcanvas, _keyboard, _display, _radio):
        self._vcanvas = _vcanvas
        self._keyboard = _keyboard
        self._display = _display
        self._radio = _radio

    async def start(self):
        ui_menu = vcanvas.Group(self._vcanvas)

        ui_settings = vcanvas.TextButton(
            ui_sidebar, text="Settings", onActivate=print)
