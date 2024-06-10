from machine import Pin
import utime
import CONSTS


class Keyboard:
    # Format is ROWCOL : [key value, key value if shifted]
    KEYS = {
        # Note: Most of row 1 is non typing keys
        '11': [" ", " "],
        # 12 - LEFT
        # 13 - UP
        # 14 - RIGHT
        # 15 - DOWN
        # 16 - VOL+
        # 17 - VOL -
        # 18 - SW1 // Not sure what that one does
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
        '36': ["\n", "\n"],  # ENTER KEY
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

    def __init__(self, sendMSG):
        self.SHIFT_PIN = Pin(28, Pin.IN, Pin.PULL_UP)

        self.last_press_time = 0
        self.last_press_time_d = 0

        self.sendMSG = sendMSG

        self.SHIFT_PIN.irq(trigger=Pin.IRQ_FALLING, handler=self.shift_pressed)

    def shift_pressed(self, pin):
        current_time = utime.ticks_ms()
        # Check if the debounce time (200 ms) has passed
        if utime.ticks_diff(current_time, self.last_press_time) > CONSTS.DEBOUNCE_TIME:
            self.sendMSG("hello world!")
            self.last_press_time = current_time
