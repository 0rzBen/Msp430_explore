
import sensor, image, time, lcd

lcd.init()                          # Init lcd display
lcd.clear(lcd.RED)                  # Clear lcd screen.

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

# binding UART1 IO:6->RX, 8->TX  //UART2 contradicts the sensor when communicate with msp430f5529
from fpioa_manager import fm
from machine import UART


fm.register(6, fm.fpioa.UART1_RX)
fm.register(8, fm.fpioa.UART1_TX)

yb_uart = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)

write_bytes = b'Hype boy yo!$'
last_time = time.ticks_ms()
tmp = 'Original'

try:
    while True:

        img = sensor.snapshot()         # Take a picture and return the image.

        # send data per 500ms


        if time.ticks_ms() - last_time > 500:
            last_time = time.ticks_ms()
            yb_uart.write(write_bytes)
        # read and print data

        if yb_uart.any():
            read_data = yb_uart.read()
            if read_data:
               img.draw_string(2,2, read_data, color=(0, 176, 80), scale=2)
               tmp = read_data
               print(read_data)


        img.draw_string(2,2, tmp, color=(0, 176, 80), scale=2)
        lcd.display(img)                # Display image on lcd.


except:
    pass

yb_uart.deinit()
del yb_uart
