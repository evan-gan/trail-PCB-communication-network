import framebuf
import time


class vCanvas(framebuf.FrameBuffer):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = bytearray(self.width * self.height // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)

    def clear(self):
        self.fill(0)


class UIElement:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        raise NotImplementedError(
            "Draw method should be implemented by subclasses")


class UILabel(UIElement):
    def __init__(self, x, y, text, font_size=1):
        super().__init__(x, y)
        self.text = text
        self.font_size = font_size

    def draw(self, canvas):
        canvas.text(self.text, self.x, self.y, 1)
