from machine import Pin, I2C
import utime
import math
from lib.ssd1306 import SSD1306_I2C


class Display:
    def __init__(self, width, height):
        self.display_width = width
        self.display_height = height

        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        self.display = SSD1306_I2C(
            self.display_width, self.display_height, self.i2c, page_addressing=False)

    def calculate_text_position(self, text, parent_size, parent_position, position, text_size):
        char_width = 5
        char_height = 8

        text_width = len(text) * char_width * text_size
        text_height = char_height * text_size  # Assuming single-line text.

        pos_x, pos_y, ax, ay, pos_type = position["x"], position[
            "y"], position["ax"], position["ay"], position["type"]

        if pos_type == "scale":
            ref_pos_x = pos_x * parent_size[0]
            ref_pos_y = pos_y * parent_size[1]
        else:
            ref_pos_x = pos_x
            ref_pos_y = pos_y

        top_left_x = int(ref_pos_x - (ax * text_width))
        top_left_y = int(ref_pos_y - (ay * text_height))

        return top_left_x, top_left_y

    def calculate_size(self, parent_size, size):
        size_x, size_y, size_type = size["x"], size["y"], size["type"]

        if size_type == "scale":
            width = size_x * parent_size[0]
            height = size_y * parent_size[1]
        else:
            width = size_x
            height = size_y

        return int(width), int(height)

    def calculate_frame_position(self, parent_size, parent_position, size, position):
        width, height = self.calculate_size(parent_size, size)
        size_type = size["type"]

        pos_x, pos_y, ax, ay, pos_type = position["x"], position[
            "y"], position["ax"], position["ay"], position["type"]

        if pos_type == "scale":
            ref_pos_x = pos_x * parent_size[0]
            ref_pos_y = pos_y * parent_size[1]
        else:
            ref_pos_x = pos_x
            ref_pos_y = pos_y

        top_left_x = int(ref_pos_x - (ax * width))
        top_left_y = int(ref_pos_y - (ay * height))

        if size_type == "scale":
            top_left_x += parent_position[0]
            top_left_y += parent_position[1]

        return top_left_x, top_left_y

    def render_component(self, prop, parent_size, parent_position=[0, 0]):
        class_name = prop["class_name"]

        if class_name == "TextLabel":
            position = prop["position"]

            text = prop["text"]

            text_size = prop["text_size"]
            text_color = prop["text_color"]

            x, y = self.calculate_text_position(
                text, parent_size, parent_position, position, text_size)

            # offset to the left a bit cuz the display is weird
            x = x - (2 * text_size)

            x += parent_position[0]
            y += parent_position[1]

            self.display.text(text, x,
                              y, text_color, size=text_size)
        elif class_name == "Frame":
            # print(parent_position, parent_size, "poopy")

            size = prop["size"]
            position = prop["position"]

            width, height = self.calculate_size(parent_size, size)
            pos_x, pos_y = self.calculate_frame_position(
                parent_size, parent_position, size, position)

            fill = prop["fill"]

            print(pos_x, pos_y, width, height)
            self.display.rect(pos_x,  pos_y, width, height, 1, fill=fill)

            if "children" in prop:
                for child_key, child_prop in prop["children"].items():
                    # print([width, height])
                    self.render_component(
                        child_prop, [width, height], [pos_x,  pos_y])

    def render(self, data):
        # print(data)

        self.display.fill(0)

        for key, prop in data.items():
            self.render_component(
                prop, [self.display_width, self.display_height])

        self.display.show()

    # def test(self):
    #     # print("TEST")
    #     if self.b == 1:
    #         self.b = 0
    #         self.update(l.idk)
    #     else:
    #         self.b = 1
    #         self.update(l.lll)
