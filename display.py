from machine import Pin, I2C
import utime
import math
from lib.ssd1306 import SSD1306_I2C


class Display:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        self.display = SSD1306_I2C(128, 64, self.i2c, page_addressing=False)
        self.b = 1

    def calculate_text_position(self, text, estate, position, size):
        char_width = 5
        char_height = 8
        text_width = len(text) * char_width * size
        text_height = char_height * size  # Assuming single-line text.

        x, y, ax, ay = position["x"], position["y"], position["ax"], position["ay"]

        if position["type"] == "scale":
            ref_x = x * estate[0]
            ref_y = y * estate[1]
        else:
            ref_x = x
            ref_y = y

        # top_left_x = int(ref_x - text_width / 2)
        top_left_x = int(ref_x - (ax * text_width))
        top_left_y = int(ref_y - (ay * text_height))

        # top_left_x = int(anchor[0] * estate[0] - text_width / 2)
        # top_left_y = int(anchor[1] * estate[1] - text_height / 2)

        return top_left_x, top_left_y

    def calculate_frame_position(self, estate, position, size):
        x, y, ax, ay = position["x"], position["y"], position["ax"], position["ay"]
        width, height = size

        if position["type"] == "scale":
            ref_x = x * estate[0]
            ref_y = y * estate[1]
        else:
            ref_x = x
            ref_y = y

        top_left_x = int(ref_x - (ax * width))
        top_left_y = int(ref_y - (ay * height))

        return top_left_x, top_left_y

    def render(self, data):
        # print(data)

        self.display.fill(0)

        for key, prop in data.items():
            # print(elem, prop)
            if prop["class_name"] == "TextLabel":
                # print("d")
                text = prop["text"]
                position = prop["position"]
                size = prop["text_size"]

                x, y = self.calculate_text_position(
                    text, [128, 64], position, size)

                # offset to the left a bit cuz the display is weird
                x = x - (2 * size)

                self.display.text(text, x,
                                  y, 1, size=prop["text_size"])
            elif prop["class_name"] == "Frame":
                # print("Frame")

                x, y = self.calculate_frame_position(
                    [128, 64], prop["position"], [prop["width"], prop["height"]])

                width, height = prop["width"], prop["height"]
                color = prop["background_color"]

                # print(x, y, width, height, color)

                self.display.rect(x, y, width, height, color)
        self.display.show()

    # def test(self):
    #     # print("TEST")
    #     if self.b == 1:
    #         self.b = 0
    #         self.update(l.idk)
    #     else:
    #         self.b = 1
    #         self.update(l.lll)
