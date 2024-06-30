from machine import Pin
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
        # '36': ENTER KEY
        '37': ["z", "Z"],
        '28': ["x", "X"],
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
        # 65 is backspace
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

    def __init__(self, sendMSG, appendToDraft, deleteLastCharOfDraft):
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

    def getShiftPressed(self):
        # Returns 1 if pressed, and 0 if not
        return 1 if self.SHIFT_PIN.value() == 0 else 0

        # if self.SHIFT_PIN.value() == 0:
        #     return 1
        # else:
        #     return 0

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

        key_values = self.KEYS.get(RowCol)

        if key_values:
            print(key_values[self.getShiftPressed()])
        elif RowCol == '36':
            print("Enter")
        elif RowCol == '65':
            print("Backspace")

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
