from machine import Pin
import utime
import CONSTS

COL_PINS = [10, 27, 6]
ROW_PINS = [14, 13, 21]

class Keyboard:
    #Format is ROWCOL : [key value, key value if shifted]
    KEYS = {
        #Note: Most of row 1 is non typing keys
        '11': [" "," "], 
        '28': ["/","?"],
        '27': [".",">"],
        '26': [",","<"],
        '25': ["m","M"],
        '24': ["n","N"],
        '23': ["b","B"],
        '22': ["v","V"],
        '21': ["c","C"],
        '31': ["j","J"],
        '32': ["k","K"],
        '33': ["l","L"],
        '34': [";",":"],
        '35': ["'",'"'],
        '36': ["\n","\n"], #ENTER KEY
        '37': ["z","Z"],
        '28': ["nonSHIFT","SHIFT"],
        'ROWCOL': ["nonSHIFT","SHIFT"],}
    KEYS2 = {
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
        "64": ["=", "+"], # 65 is backspace
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
    }

    def __init__(self, sendMSG):
        for pin in COL_PINS:
            Pin(pin, Pin.IN, Pin.PULL_UP)

        for pin in ROW_PINS:
            Pin(pin, Pin.IN, Pin.PULL_UP)
        
        self.SHIFT_PIN = Pin(28, Pin.IN, Pin.PULL_UP)
        self.COL_GS_PIN = Pin(7, Pin.IN)
        self.ROW_GS_PIN = Pin(9, Pin.IN, Pin.PULL_UP)
        
        self.last_press_time = 0
        self.last_press_time_d = 0

        self.sendMSG = sendMSG

        Pin(COL_PINS[0], Pin.IN, Pin.PULL_UP).irq(trigger=Pin.IRQ_FALLING, handler=self.keypor)
        self.COL_GS_PIN.irq(trigger=Pin.IRQ_FALLING, handler=self.keypor)
        self.SHIFT_PIN.irq(trigger=Pin.IRQ_FALLING, handler=self.shift_pressed)


    def shift_pressed(self, pin):
        current_time = utime.ticks_ms()
        # Check if the debounce time (200 ms) has passed
        if utime.ticks_diff(current_time, self.last_press_time) > CONSTS.DEBOUNCE_TIME:
            self.sendMSG("hello world!")
            self.last_press_time = current_time
    
    def keypor(self, pin):
        current_time = utime.ticks_ms()
        # Check if the debounce time (200 ms) has passed
        if utime.ticks_diff(current_time, self.last_press_time_d) > CONSTS.DEBOUNCE_TIME:
            print("Key pressed", current_time)
            self.last_press_time_d = current_time