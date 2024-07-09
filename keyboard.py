from machine import Pin
import uasyncio
import utime

import CONSTS


class Keyboard:
    # Format is ROWCOL : [key value, key value if shifted]
    KEYS = {
        # Note: Most of Col 1 is non typing keys
        '11': [" ", " "],
        # '12' - LEFT
        # '13' - UP
        # '14' - RIGHT
        # '15' - DOWN
        '16': [" ", " "],
        '17': [" ", " "],
        '18': [" ", " "],
        '28': ["/", "?"],
        '27': [".", ">"],
        '26': [",", "<"],
        '25': ["m", "M"],
        '24': ["n", "N"],
        '23': ["b", "B"],
        '22': ["v", "V"],
        '21': ["c", "C"],
        '31': ["j", "J"],
        '32': ["k", "K"],
        '33': ["l", "L"],
        '34': [";", ":"],
        '35': ["'", '"'],
        '37': ["z", "Z"],
        '38': ["x", "X"],
        "71": ["1", "!"],
        "72": ["2", "@"],
        "73": ["3", "#"],
        "74": ["4", "$"],
        "75": ["5", "%"],
        "76": ["6", "^"],
        "77": ["7", "&"],
        "78": ["8", "*"],
        "61": ["9", "("],
        "62": ["0", ")"],
        "63": ["-", "_"],
        "64": ["=", "+"],
        "66": ["q", "Q"],
        "67": ["w", "W"],
        "68": ["e", "E"],
        "51": ["r", "R"],
        "52": ["t", "T"],
        "53": ["y", "Y"],
        "54": ["u", "U"],
        "55": ["i", "I"],
        "56": ["o", "O"],
        "57": ["p", "P"],
        "58": ["[", "{"],
        "41": ["]", "}"],
        "42": ["\\", "|"],
        "43": ["a", "A"],
        "44": ["s", "S"],
        "45": ["d", "D"],
        "46": ["f", "F"],
        "47": ["g", "G"],
        "48": ["h", "H"]
    }

    # actionKeys = {
    #     "BACKSPACE": "65",
    #     "ENTER": "36",

    #     "LEFT": "12",
    #     "UP": "13",
    #     "RIGHT": "14",
    #     "DOWN": "15"
    # }

    actionKeys = {
        "65": "Backspace",
        "36": "Enter",
        "12": "Left",
        "13": "Up",
        "14": "Right",
        "15": "Down",
    }

    pull_downs = {
        "Col1": 6,
        "Col2": 7,
        "Col3": 8,
        "Col4": 9,
        "Col5": 13,
        "Col6": 14,
        "Col7": 5,
        "Col8": 4,

        "Row1": 27,
        "Row2": 26,
        "Row3": 22,
        "Row4": 21,
        "Row5": 19,
        "Row6": 18,
        "Row7": 17,
    }

    pull_ups = {
        "SHIFT": 28
    }

    keys_cooldown = {}

    one_time_callbacks = {}

    def __init__(self, _vcanvas, onKeyPress, onLeft, onUp, onRight, onDown):
        self._vcanvas = _vcanvas
        self.onKeyPress = onKeyPress

        self.onLeft = onLeft
        self.onUp = onUp
        self.onRight = onRight
        self.onDown = onDown

        self.focused_element = None

        for key, value in self.pull_downs.items():
            setattr(self, key, Pin(value, Pin.IN, Pin.PULL_DOWN))

        for key, value in self.pull_ups.items():
            setattr(self, key, Pin(value, Pin.IN, Pin.PULL_UP))

        # Set up the interrupts on the rising edge (button press) for each pin
        for key, value in self.pull_downs.items():
            getattr(self, key).irq(trigger=Pin.IRQ_RISING,
                                   handler=self.handleKeyPress)

        self.SHIFT_PIN = Pin(28, Pin.IN, Pin.PULL_UP)

        self.last_press_time = 0

    def jumpToElement(self, direction):
        components = self._vcanvas.components  # Assuming we have a reference to vCanvas
        keys = list(components.keys())

        def find_next_focusable(start_index, step):
            index = start_index

            for _ in range(len(keys)):
                index = (index + step) % len(keys)
                component = components[keys[index]]

                if component.get('focusable', False):
                    return component

            return None  # No focusable element found

        if not self.focused_element:
            # If no element is focused, find the first focusable element
            next_component = find_next_focusable(-1, 1)
        else:
            current_key = self.focused_element.key
            current_index = keys.index(current_key)

            if direction == "Right":
                next_component = find_next_focusable(current_index, 1)
            elif direction == "Left":
                next_component = find_next_focusable(current_index, -1)
            else:
                return  # Invalid direction

        if next_component:
            self.focused_element = next_component

            # Optionally, add visual feedback for the new focused element
            if hasattr(self.focused_element, 'on_focus'):
                self.focused_element.on_focus()
        else:
            print("No focusable elements found")

    def onceKeyPress(self, key, cb):
        self.one_time_callbacks[key] = cb

    def checkKeyCooldown(self, RowCol):
        current_time = utime.ticks_ms()

        return utime.ticks_diff(current_time, self.keys_cooldown.get(RowCol, CONSTS.KEYBOARD_DEBOUNCE_TIME_MS + 1)) > CONSTS.KEYBOARD_DEBOUNCE_TIME_MS

    def handleKeyPress(self, pin):
        # print("Called!", pin)

        RowCol = self.getRowPressed() + self.getColPressed()

        if "0" in RowCol:
            return

        # Check if the debounce time (150 ms) has passed, if it has not return
        if self.checkKeyCooldown(RowCol):
            self.keys_cooldown[RowCol] = utime.ticks_ms()
        else:
            return

        if "" in self.one_time_callbacks:
            self.one_time_callbacks[""]()
            del self.one_time_callbacks[""]
        elif RowCol in self.one_time_callbacks:
            self.one_time_callbacks[RowCol]()
            del self.one_time_callbacks[RowCol]

        # print(f"{RowCol} was pressed!")

        action = self.actionKeys.get(RowCol)

        if action:
            if self.focused_element:
                if action == "Backspace":
                    if hasattr(self.focused_element, "text"):
                        self.focused_element.text = self.focused_element.text[:-1]
                elif action == "Enter":
                    if hasattr(self.focused_element, "onEnter"):
                        self.focused_element.onEnter()
                    elif hasattr(self.focused_element, "onActivate"):
                        self.focused_element.onActivate()
                elif action in ["Left", "Up", "Right", "Down"]:
                    if action in ["Up", "Down"] and self.focused_element.class_name == "ScrollingFrame":
                        self.focused_element.scroll(action)

                    if action in ["Left", "Right"]:
                        self.jumpToElement(action)

            else:
                # TODO: Lol
                # getattr(self, f"on{action}")()
                pass

            return

        key = self.KEYS.get(RowCol)

        if key:
            if self.focused_element:
                new_text = self.focused_element.text + \
                    key[1 if self.SHIFT_PIN.value() == 0 else 0]

                if len(new_text) <= self.focused_element.text_limit or self.focused_element.text_limit == -1:
                    self.focused_element.text = new_text
            # else:
            #     self.onKeyPress(
            #         key[1 if self.SHIFT_PIN.value() == 0 else 0])

    def getColPressed(self):
        cols = {k: v for k, v in self.pull_downs.items() if k.startswith("Col")}

        for col in cols:
            if getattr(self, col).value() == 1:
                return col.split("Col")[1]

        return "0"

    def getRowPressed(self):
        rows = {k: v for k, v in self.pull_downs.items() if k.startswith("Row")}

        for row in rows:
            if getattr(self, row).value() == 1:
                return row.split("Row")[1]

        return "0"

    def setFocus(self, element):
        self.focused_element = element
