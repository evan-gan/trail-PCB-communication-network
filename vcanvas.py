# Creates a virtual canvas that serves as an intermediary layer between the UI elements and the real display.

# TODO: Improve update logic in UIComponent so that it doesnt reconstruct the entire data object every time a property is updated (for efficiency)
# TODO: Fool-check the recursive container update logic cuz i kinda just wrote it without thinking too much
# TODO: Add more UI components (Scrolling frame, buttons, etc)
# TODO: Check the remove and update methods in vCanvas again cuz like the #2 todo i kinda rushed it

import time
import utime

import uasyncio as asyncio
# import _thread

import lib.cframebuf as framebuf
import lib.utils as utils


class vCanvas:
    def __init__(self, width, height, renderCb):
        self.display_width = width
        self.display_height = height

        self.renderCb = renderCb

        self.data = {}

    def remove(self, key):
        if key in self.data:
            del self.data[key]

    def update(self, key, data):
        self.data[key] = data

    async def render(self):
        while True:
            await asyncio.sleep(1/60)
            self.renderCb(self.data)


class PropertyDescriptor:
    def __init__(self, name, type_, *, default=None, immutable=False):
        self.name = name
        self.type = type_
        self.default = default  # corrected to use default value
        self.immutable = immutable
        self.private_name = '_' + name  # Explicitly set the private_name

    # def __set_name__(self, owner, name):
    #     self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name, self.default)

    def __set__(self, obj, value):
        if hasattr(obj, self.private_name) and self.immutable:
            raise AttributeError(
                f"{self.name} is immutable and cannot be altered once set.")

        if not isinstance(value, self.type):
            raise TypeError(
                f"Expected {self.name} to be {self.type.__name__}, got {type(value).__name__}")

        setattr(obj, self.private_name, value)

        # Update the container if it exists
        if hasattr(obj, "update_container"):
            obj.update_container()


class UIComponent:
    class_name = PropertyDescriptor("class_name", str, immutable=True)

    x = PropertyDescriptor("x", (int, float), default=0)
    y = PropertyDescriptor("y", (int, float), default=0)

    ax = PropertyDescriptor("ax", (int, float), default=0)
    ay = PropertyDescriptor("ay", (int, float), default=0)

    position_type = PropertyDescriptor(
        "position_type", str, default="offset")

    def __init__(self, container, **kwargs):
        self.key = utils.random_string(8)
        self.container = container
        self.children = {}
        self.class_name = self.__class__.__name__

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.update_container()

    def update(self, key, data):
        self.children[key] = data
        self.update_container()

    def update_container(self):
        data = {}

        # Collect all properties from UIComponent and its subclasses
        for cls in [UIComponent, self.__class__]:
            for key, descriptor in cls.__dict__.items():
                if isinstance(descriptor, PropertyDescriptor):
                    data[key] = getattr(self, key)

        # Format position data
        data["position"] = {
            "x": data.pop("x"),
            "y": data.pop("y"),
            "ax": data.pop("ax"),
            "ay": data.pop("ay"),
            "type": data.pop("position_type"),
        }

        if "width" in data and "height" in data:
            data["size"] = {
                "x": data.pop("width"),
                "y": data.pop("height"),
                "type": data.pop("size_type"),
            }

        if self.children:
            data["children"] = self.children

        self.container.update(self.key, data)


class Frame(UIComponent):
    size_type = PropertyDescriptor("size_type", str, default="offset")

    width = PropertyDescriptor("width", (int, float), default=10)
    height = PropertyDescriptor("height", (int, float), default=10)

    fill = PropertyDescriptor("fill", bool, default=False)

    # def __init__(self, container, data):
    #     super().__init__(container, data, class_name="Frame")


class TextLabel(UIComponent):
    text = PropertyDescriptor("text", str, default="")

    text_size = PropertyDescriptor("text_size", int, default=1)
    text_color = PropertyDescriptor("text_color", int, default=1)

    # def __init__(self, container, data):
    #     super().__init__(container, data, class_name="TextLabel")
