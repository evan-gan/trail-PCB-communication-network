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

    focused_element = None

    def __init__(self, onKeyPress, onEnter, onBackspace, onLeft, onUp, onRight, onDown):
        self.onKeyPress = onKeyPress

        self.onEnter = onEnter
        self.onBackspace = onBackspace

        self.onLeft = onLeft
        self.onUp = onUp
        self.onRight = onRight
        self.onDown = onDown

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

    async def listenForBackspace(self):
        while True:
            await uasyncio.sleep(1/30)
            

    def handleKeyPress(self, pin):
        # print("Called!", pin)

        RowCol = self.getRowPressed() + self.getColPressed()

        if "0" in RowCol:
            return

        current_time = utime.ticks_ms()

        # Check if the debounce time (150 ms) has passed, if it has not return
        if utime.ticks_diff(current_time, self.keys_cooldown.get(RowCol, CONSTS.KEYBOARD_DEBOUNCE_TIME_MS + 1)) > CONSTS.KEYBOARD_DEBOUNCE_TIME_MS:
            self.keys_cooldown[RowCol] = current_time
        else:
            return

        # print(f"{RowCol} was pressed!")

        action = self.actionKeys.get(RowCol)

        if action:
            getattr(self, f"on{action}")()

            return

        key = self.KEYS.get(RowCol)

        if key:
            self.onKeyPress(
                key[1 if self.SHIFT_PIN.value() == 0 else 0])

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
