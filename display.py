from machine import Pin, I2C
import utime
import math
from lib.ssd1306 import SSD1306_I2C


class Display:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        self.display = SSD1306_I2C(128, 64, self.i2c, page_addressing=False)
        self.b = 1

    def calculate_text_position(self, text, parent_size, position, text_size):
        char_width = 5
        char_height = 8

        text_width = len(text) * char_width * text_size
        text_height = char_height * text_size  # Assuming single-line text.

        x, y, ax, ay = position["x"], position["y"], position["ax"], position["ay"]

        if position["type"] == "scale":
            ref_x = x * parent_size[0]
            ref_y = y * parent_size[1]
        else:
            ref_x = x
            ref_y = y

        top_left_x = int(ref_x - (ax * text_width))
        top_left_y = int(ref_y - (ay * text_height))

        return top_left_x, top_left_y

    def calculate_frame_position(self, parent_size, position, size):
        x, y, ax, ay = position["x"], position["y"], position["ax"], position["ay"]
        width, height = size

        if position["type"] == "scale":
            ref_x = x * parent_size[0]
            ref_y = y * parent_size[1]
        else:
            ref_x = x
            ref_y = y

        top_left_x = int(ref_x - (ax * width))
        top_left_y = int(ref_y - (ay * height))

        return top_left_x, top_left_y

    def render_component(self, prop, parent_size, parent_position=[0, 0]):
        class_name = prop["class_name"]

        if class_name == "TextLabel":
            text = prop["text"]
            position = prop["position"]
            text_size = prop["text_size"]

            x, y = self.calculate_text_position(
                text, parent_size, position, text_size)

            # offset to the left a bit cuz the display is weird
            x = x - (2 * text_size)

            x += parent_position[0]
            y += parent_position[1]

            self.display.text(text, x,
                              y, 1, size=text_size)
        elif class_name == "Frame":
            position = prop["position"]
            width, height = prop["width"], prop["height"]

            x, y = self.calculate_frame_position(
                parent_size, position, [width, height])

            color = prop["background_color"]

            self.display.rect(x, y, width, height, color)

            if "children" in prop:
                for child_key, child_prop in prop["children"].items():
                    self.render_component(child_prop, [width, height], [x, y])

    def render(self, data):
        print(data)

        self.display.fill(0)

        for key, prop in data.items():
            self.render_component(prop, [128, 64])

        self.display.show()

    # def test(self):
    #     # print("TEST")
    #     if self.b == 1:
    #         self.b = 0
    #         self.update(l.idk)
    #     else:
    #         self.b = 1
    #         self.update(l.lll)
