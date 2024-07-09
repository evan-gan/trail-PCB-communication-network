import uasyncio

import vcanvas

import CONSTS


class UI_Home:
    def __init__(self, _vcanvas, _keyboard, _display, _radio):
        self._vcanvas = _vcanvas
        self._keyboard = _keyboard
        self._display = _display
        self._radio = _radio

    async def start(self):
        # ui_channels = vcanvas.ScrollingFrame(self._vcanvas, width=1,
        #                                      height=1, size_type="scale", border=False, visible=False)

        ui_settings = vcanvas.Frame(
            self._vcanvas, width=1, height=1, size_type="scale", border=False, visible=True)

        ui_settings_exit = vcanvas.TextButton(
            ui_settings, text="< Back", x=5, y=5, onActivate=print, style="underline")

        ui_settings_title = vcanvas.TextLabel(
            ui_settings, text="Settings", x=CONSTS.DISPLAY_WIDTH - 5, y=5, ax=1, text_wrap=False)
