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

    def __init__(self, sendMSG, appendToDraft, deleteLastCharOfDraft):
        self.Col1 = Pin(6, Pin.IN, Pin.PULL_DOWN)
        self.Col2 = Pin(7, Pin.IN, Pin.PULL_DOWN)
        self.Col3 = Pin(8, Pin.IN, Pin.PULL_DOWN)
        self.Col4 = Pin(9, Pin.IN, Pin.PULL_DOWN)
        self.Col5 = Pin(13, Pin.IN, Pin.PULL_DOWN)
        self.Col6 = Pin(14, Pin.IN, Pin.PULL_DOWN)
        self.Col7 = Pin(5, Pin.IN, Pin.PULL_DOWN)
        self.Col8 = Pin(4, Pin.IN, Pin.PULL_DOWN)

        self.Row1 = Pin(27, Pin.IN, Pin.PULL_DOWN)
        self.Row2 = Pin(26, Pin.IN, Pin.PULL_DOWN)
        self.Row3 = Pin(22, Pin.IN, Pin.PULL_DOWN)
        self.Row4 = Pin(21, Pin.IN, Pin.PULL_DOWN)
        self.Row5 = Pin(19, Pin.IN, Pin.PULL_DOWN)
        self.Row6 = Pin(18, Pin.IN, Pin.PULL_DOWN)
        self.Row7 = Pin(17, Pin.IN, Pin.PULL_DOWN)

        # Set up the interrupts on the rising edge (button press) for each pin
        self.Col1.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Col2.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Col3.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Col4.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Col5.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Col6.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Col7.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Col8.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)

        self.Row1.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Row2.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Row3.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Row4.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Row5.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Row6.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)
        self.Row7.irq(trigger=Pin.IRQ_RISING, handler=self.handleKeyPress)

        self.SHIFT_PIN = Pin(28, Pin.IN, Pin.PULL_UP)

        self.last_press_time = 0
        # self.last_press_time_d = 0

        #Append text to draft
        self.appendToDraft = appendToDraft
        #Delete the last letter added to the draft
        self.deleteLastCharOfDraft = deleteLastCharOfDraft
        #Function to send a message when enter is pressed
        self.sendMSG = sendMSG

        # self.SHIFT_PIN.irq(trigger=Pin.IRQ_FALLING, handler=self.shift_pressed)

    def getShiftPressed(self):
        #Returns 1 if pressed, and 0 if not
        if self.SHIFT_PIN.value() == 0:
            return 1
        else:
            return 0

    def handleKeyPress(self, pin):
        print("Called!")
        current_time = utime.ticks_ms()
        # Check if the debounce time (200 ms) has passed, if it has not return
        if utime.ticks_diff(current_time, self.last_press_time) > CONSTS.DEBOUNCE_TIME:
            self.last_press_time = current_time
        else:
            return

        RowCol = self.getRowColPressed()
        print(f"{RowCol} was pressed!")
        if self.KEYS.get(RowCol, "nil") != "nil":
            self.appendToDraft((self.KEYS.get(RowCol))[self.getShiftPressed()]) # type: ignore
        elif RowCol == '36':
            self.sendMSG()
        elif RowCol == '65':
            self.deleteLastCharOfDraft()

    def getRowColPressed(self):
        return str(self.getRowPressed()) + str(self.getColPressed())

    def getColPressed(self):
        if self.Col1.value() == 1:
            return 1
        elif self.Col2.value() == 1:
            return 2
        elif self.Col3.value() == 1:
            return 3
        elif self.Col4.value() == 1:
            return 4
        elif self.Col5.value() == 1:
            return 5
        elif self.Col6.value() == 1:
            return 6
        elif self.Col7.value() == 1:
            return 7
        elif self.Col8.value() == 1:
            return 8

    def getRowPressed(self):
        if self.Row1.value() == 1:
            return 1
        elif self.Row2.value() == 1:
            return 2
        elif self.Row3.value() == 1:
            return 3
        elif self.Row4.value() == 1:
            return 4
        elif self.Row5.value() == 1:
            return 5
        elif self.Row6.value() == 1:
            return 6
        elif self.Row7.value() == 1:
            return 7
def dummyFunc(input):
    print(input)
keyboard = Keyboard(dummyFunc,dummyFunc,dummyFunc)

while True:
    utime.sleep(1)
    print("Running...")
