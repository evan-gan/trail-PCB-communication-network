# Creates a virtual canvas that serves as an intermediary layer between the UI elements and the real display.

import time
import utime

import uasyncio as asyncio
# import _thread

import lib.cframebuf as framebuf
import lib.utils as utils


class vCanvas:
    def __init__(self, width, height, renderCb):
        self.width = width
        self.height = height
        self.renderCb = renderCb

        self.data = {}

    def remove(self, key):
        del self.data[key]

    def update(self, key, data):
        self.data[key] = data

    async def render(self):
        while True:
            await asyncio.sleep(1/60)
            self.renderCb(self.data)


class TextLabel:
    def __init__(self, container, data):
        self.container = container

        self.key = utils.random_string(8)
        data["className"] = "TextLabel"
        self.data = data

        self.container.update(self.key, data)

    @property
    def text(self):
        return self.data["text"]

    @property
    def text_size(self):
        return self.data["text_size"]

    @property
    def x(self):
        return self.data["position"]["x"]

    @property
    def y(self):
        return self.data["position"]["y"]

    @property
    def ax(self):
        return self.data["position"]["ax"]

    @property
    def ay(self):
        return self.data["position"]["ay"]

    @property
    def position_type(self):
        return self.data["position"]["type"]

    @text.setter
    def text(self, value):
        self.data["text"] = value
        self.container.update(self.key, self.data)

    @text_size.setter
    def text_size(self, value):
        self.data["text_size"] = value
        self.container.update(self.key, self.data)

    @x.setter
    def x(self, value):
        self.data["position"]["x"] = value
        self.container.update(self.key, self.data)

    @y.setter
    def y(self, value):
        self.data["position"]["y"] = value
        self.container.update(self.key, self.data)

    @ax.setter
    def ax(self, value):
        self.data["position"]["ax"] = value
        self.container.update(self.key, self.data)

    @ay.setter
    def ay(self, value):
        self.data["position"]["ay"] = value
        self.container.update(self.key, self.data)

    @position_type.setter
    def position_type(self, value):
        self.data["position"]["type"] = value
        self.container.update(self.key, self.data)
