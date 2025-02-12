from machine import Pin
# import uasyncio
import utime

import CONSTS
def defaultLambda():
    print("Default lambda was called")

class Keyboard:
    # Format is ROWCOL : [key value, key value if shifted]
    KEYS:dict[str, list[str]] = {
        # Note: Most of Col 1 is non typing keys
        '11': [" ", " "], # type: ignore
        # '12' - LEFT
        # '13' - UP
        # '14' - RIGHT
        # '15' - DOWN
        '16': [" ", " "], # type: ignore
        '17': [" ", " "], # type: ignore
        '18': [" ", " "], # type: ignore
        '28': ["/", "?"], # type: ignore
        '27': [".", ">"], # type: ignore
        '26': [",", "<"], # type: ignore
        '25': ["m", "M"], # type: ignore
        '24': ["n", "N"], # type: ignore
        '23': ["b", "B"], # type: ignore
        '22': ["v", "V"], # type: ignore
        '21': ["c", "C"], # type: ignore
        '31': ["j", "J"], # type: ignore
        '32': ["k", "K"], # type: ignore
        '33': ["l", "L"], # type: ignore
        '34': [";", ":"], # type: ignore
        '35': ["'", '"'], # type: ignore
        '37': ["z", "Z"], # type: ignore
        '38': ["x", "X"], # type: ignore
        "71": ["1", "!"], # type: ignore
        "72": ["2", "@"], # type: ignore
        "73": ["3", "#"], # type: ignore
        "74": ["4", "$"], # type: ignore
        "75": ["5", "%"], # type: ignore
        "76": ["6", "^"], # type: ignore
        "77": ["7", "&"], # type: ignore
        "78": ["8", "*"], # type: ignore
        "61": ["9", "("], # type: ignore
        "62": ["0", ")"], # type: ignore
        "63": ["-", "_"], # type: ignore
        "64": ["=", "+"], # type: ignore
        "66": ["q", "Q"], # type: ignore
        "67": ["w", "W"], # type: ignore
        "68": ["e", "E"], # type: ignore
        "51": ["r", "R"], # type: ignore
        "52": ["t", "T"], # type: ignore
        "53": ["y", "Y"], # type: ignore
        "54": ["u", "U"], # type: ignore
        "55": ["i", "I"], # type: ignore
        "56": ["o", "O"], # type: ignore
        "57": ["p", "P"], # type: ignore
        "58": ["[", "{"], # type: ignore
        "41": ["]", "}"], # type: ignore
        "42": ["\\", "|"], # type: ignore
        "43": ["a", "A"], # type: ignore
        "44": ["s", "S"], # type: ignore
        "45": ["d", "D"], # type: ignore
        "46": ["f", "F"], # type: ignore
        "47": ["g", "G"], # type: ignore
        "48": ["h", "H"] # type: ignore
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
        "65": "Backspace", # type: ignore
        "36": "Enter", # type: ignore
        "12": "Left", # type: ignore
        "13": "Up", # type: ignore
        "14": "Right", # type: ignore
        "15": "Down", # type: ignore
    }

    pull_downs = {
        "Col1": 6, # type: ignore
        "Col2": 7, # type: ignore
        "Col3": 8, # type: ignore
        "Col4": 9, # type: ignore
        "Col5": 13, # type: ignore
        "Col6": 14, # type: ignore
        "Col7": 5, # type: ignore
        "Col8": 4, # type: ignore

        "Row1": 27, # type: ignore
        "Row2": 26, # type: ignore
        "Row3": 22, # type: ignore
        "Row4": 21, # type: ignore
        "Row5": 19, # type: ignore
        "Row6": 18, # type: ignore
        "Row7": 17, # type: ignore
    }

    pull_ups = {
        "SHIFT": 28 # type: ignore
    }

    keys_cooldown = {}

    def __init__(self, onKeyPress, onEnter, onBackspace, scrollUp, scrollDown): #onKeyPress, onLeft, onUp, onRight, onDown

        self.onKeyPress = onKeyPress
        self.onEnter = onEnter
        self.onBackspace = onBackspace
        #Scroll stuff:
        self.scrollUp = scrollUp
        self.scrollDown = scrollDown

        #Set pull downs
        for key, value in self.pull_downs.items():
            setattr(self, key, Pin(value, Pin.IN, Pin.PULL_DOWN))

        #Set pull ups
        for key, value in self.pull_ups.items():
            setattr(self, key, Pin(value, Pin.IN, Pin.PULL_UP))

        # Set up the interrupts on the rising edge (button press) for each pin
        for key, value in self.pull_downs.items():
            getattr(self, key).irq(trigger=Pin.IRQ_RISING,handler=self.handleKeyPress)

        self.SHIFT_PIN = Pin(28, Pin.IN, Pin.PULL_UP)

    def hasCooldownPassed(self, RowCol):
        current_time = utime.ticks_ms()

        return utime.ticks_diff(current_time, self.keys_cooldown.get(RowCol, CONSTS.KEYBOARD_DEBOUNCE_TIME_MS + 1)) > CONSTS.KEYBOARD_DEBOUNCE_TIME_MS

    def handleKeyPress(self, pin):
        # print("Called!", pin)

        RowCol = self.getRowPressed() + self.getColPressed()
        #Double check if key has actualy been pressed
        if "0" in RowCol:
            return

        # Check if the debounce time for the RowCol has passed, if it has not return
        if self.hasCooldownPassed(RowCol):
            self.keys_cooldown[RowCol] = utime.ticks_ms()
        else:
            return

        # print(f"{RowCol} was pressed!")

        #Has an action been called?
        action = self.actionKeys.get(RowCol)

        if action:
            if action == "Backspace":
                self.onBackspace()
            elif action == "Enter":
                self.onEnter()
            elif action == "Down":
                self.scrollDown()
            elif action == "Up":
                self.scrollUp()

        #Has a keypress been called
        key = self.KEYS.get(RowCol)

        if key:
            self.onKeyPress(key[1 if self.SHIFT_PIN.value() == 0 else 0])

    def getRowColPressed(self):
        return self.getRowPressed() + self.getColPressed()

    def getColPressed(self):
        #Seperates out cols into a dictionary
        cols = {k: v for k, v in self.pull_downs.items() if k.startswith("Col")}

        for col in cols:
            #If a button is pressed, the col label is seperated so just the number exists as a string
            if getattr(self, col).value() == 1:
                return col.split("Col")[1]

        return "0"

    def getRowPressed(self):
        #Seperates out rows into a dictionary
        rows = {k: v for k, v in self.pull_downs.items() if k.startswith("Row")}

        for row in rows:
            #If a button is pressed, the row label is seperated so just the number exists as a string
            if getattr(self, row).value() == 1:
                return row.split("Row")[1]

        return "0"

