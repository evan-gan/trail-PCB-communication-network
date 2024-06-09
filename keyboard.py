from machine import Pin
import utime
import CONSTS

COL_PINS = [10, 27, 6]
ROW_PINS = [14, 13, 21]

class Keyboard:
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