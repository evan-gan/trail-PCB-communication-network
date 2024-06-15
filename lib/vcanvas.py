# Creates a virtual canvas that serves as an intermediary layer between the UI elements and the real display.

import lib.cframebuf as framebuf
import time
import utime
# import _thread

import lib.utils as utils


class vCanvas:
    def __init__(self, width, height, updateFunc):
        self.width = width
        self.height = height
        self.data = {}
        self.updateFunc = updateFunc

        # self.idk = {
        #     "TextLabel": {
        #         "position": {
        #             "type": "scale",
        #             "x": 0.5,
        #             "y": 0.5,
        #             "ax": 0.5,
        #             "ay": 0.5
        #         },
        #         "text": "Welcome!",
        #         "textSize": 1,
        #     }
        # }
        # self.lll = {
        #     "TextLabel": {
        #         "position": {
        #             "type": "offset",
        #             "x": 64,
        #             "y": 32,
        #             "ax": 0.5,
        #             "ay": 0.5
        #         },
        #         "text": "Welcome",
        #         "textSize": 1,
        #     }
        # }

    def remove(self, key):
        del self.data[key]

    def update(self, key, data):
        self.data[key] = data
        # self.updateFunc(self.data)

    def thread_function(self, name, delay):
        while True:
            utime.sleep(1/120)
            self.updateFunc(self.data)


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
