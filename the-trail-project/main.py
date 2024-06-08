from machine import Pin, I2C
import lib.ssd1306 as ssd1306
import utime

# Define the screen dimensions
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# Define the I2C pins
OLED_SDA = 0
OLED_SCL = 1

transistor = Pin(16, Pin.OUT)

transistor.high()

pin = Pin("LED", Pin.OUT)

# Initialize I2C
i2c = I2C(0, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)

# Function to scan I2C devices
def scan_i2c():
    devices = i2c.scan()
    if devices:
        print("I2C devices found:", [hex(device) for device in devices])
    else:
        print("No I2C devices found")

# Run I2C scan to check for connected devices and their addresses
scan_i2c()

# Assuming the address is correct (default 0x3C)
oled_address = 0x3c  # You may need to change this based on the scan result

# Create an SSD1306 display object
display = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c, addr=oled_address)

# Function to display text
def display_text():
    display.fill(0)  # Clear the buffer

    # Set text size and color (SSD1306 is monochrome, so only color is white)
    display.text("Hello, World!", 0, 0)
    display.text("wwwwwwwwwwwwwwwwwwwww", 0, 10)
    display.text("dbaihwdnd", 0, 20)

    # Display everything on the screen
    display.show()

# Setup function
def setup():
    print("Initializing I2C...")
    scan_i2c()
    print("Initializing OLED display...")
    
    if display.width != SCREEN_WIDTH or display.height != SCREEN_HEIGHT:
        print("SSD1306 allocation failed")
        while True:
            pass
    
    print("Clearing display...")
    display_text()
    print("Display updated with text.")

# Main loop function
def loop():
    while True:
        utime.sleep(0.1)  # Short delay to avoid spamming

# Run the setup function once
setup()

# Run the loop function indefinitely
loop()
