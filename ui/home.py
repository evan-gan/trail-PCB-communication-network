import uasyncio

import vcanvas
import typewriter


class UI_Greet:
    def __init__(self, _vcanvas, name):
        self._vcanvas = _vcanvas
        self.name = name

    async def start(self):
        
