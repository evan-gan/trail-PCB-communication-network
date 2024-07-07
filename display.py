from machine import Pin, I2C
import utime
import math
import uasyncio
from lib.ssd1306 import SSD1306_I2C
import CONSTS


class Display:
    def __init__(self, width, height):
        self.display_width = width
        self.display_height = height

        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        self.display = SSD1306_I2C(
            self.display_width, self.display_height, self.i2c, page_addressing=False)

    def clear(self):
        self.display.fill(0)
        self.display.show()

    def calculate_text_position(self, text, parent_size, parent_position, position, text_size):
        text_width = max(len(line)
                         for line in text.split("\n")) * CONSTS.CHAR_WIDTH * text_size
        text_height = len(text.split("\n")) * CONSTS.CHAR_HEIGHT * text_size

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

        # offset to the left a bit cuz the display is weird
        top_left_x = top_left_x - (2 * text_size)

        top_left_x += parent_position[0]
        top_left_y += parent_position[1]

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

    def wrap_text(self, text, available_width):
        lines = []
        current_line = ""
        current_width = 0

        for char in text:
            if current_width + CONSTS.CHAR_WIDTH <= available_width:
                current_line += char
                current_width += CONSTS.CHAR_WIDTH
            else:
                lines.append(current_line)

                current_line = char
                current_width = CONSTS.CHAR_WIDTH

        if current_line:
            lines.append(current_line)

        return '\n'.join(lines)

    def render_component(self, prop, parent_size, parent_position=[0, 0]):
        # print("Render compoent", prop)

        if not prop.get("visible", True):
            return

        class_name = prop["class_name"]

        if class_name == "TextLabel" or class_name == "TextBox":
            position = prop["position"]
            text = prop["text"]
            text_size = prop["text_size"]
            text_color = prop["text_color"]

            x, y = self.calculate_text_position(
                text, parent_size, parent_position, position, text_size)

            # Calculate available width for text
            available_width = (CONSTS.DISPLAY_WIDTH - x -
                               CONSTS.CHAR_WIDTH) - (5 * 4)  # Minus 4 characters
            # Wrap text
            wrapped_text = self.wrap_text(text, available_width)
            wrapped_lines_num = len(wrapped_text.split('\n'))

            if y + (wrapped_lines_num * CONSTS.CHAR_HEIGHT * text_size) > self.display_height:
                y = self.display_height - \
                    (wrapped_lines_num * CONSTS.CHAR_HEIGHT * text_size)

            # # Render each line of wrapped text
            # for i, line in enumerate(wrapped_text.split('\n')):
            #     self.display.text(line, x,
            #                       y + i * CONSTS.CHAR_HEIGHT * text_size,
            #                       text_color, size=text_size)

            # Render wrapped text with \n
            self.display.text(wrapped_text, x, y, text_color, size=text_size)
        elif class_name == "Frame":
            size = prop["size"]
            position = prop["position"]

            width, height = self.calculate_size(parent_size, size)
            pos_x, pos_y = self.calculate_frame_position(
                parent_size, parent_position, size, position)

            fill = prop["fill"]

            self.display.rect(pos_x,  pos_y, width, height, 1, fill=fill)

            if "children" in prop:
                for child_key, child_prop in prop["children"].items():
                    self.render_component(
                        child_prop, [width, height], [pos_x,  pos_y])
        elif class_name == "Group":
            if "children" in prop:
                for child_key, child_prop in prop["children"].items():
                    self.render_component(
                        child_prop, parent_size, parent_position)

    def render(self, data):
        # print(data)

        self.display.fill(0)

        for key, prop in data.items():
            self.render_component(
                prop, [self.display_width, self.display_height])

        self.display.show()
