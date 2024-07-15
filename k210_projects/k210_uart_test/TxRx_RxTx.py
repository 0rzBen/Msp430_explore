
import sensor, image, time, lcd, sys

lcd.init()                          
lcd.clear(lcd.WHITE)             
sensor.reset()                      
sensor.set_pixformat(sensor.RGB565) 
sensor.set_framesize(sensor.QVGA)   
sensor.skip_frames(time = 2000)    
clock = time.clock()               
from fpioa_manager import fm
from machine import UART


fm.register(6, fm.fpioa.UART1_RX)
fm.register(8, fm.fpioa.UART1_TX)

uart = UART(UART.UART1, 9600, read_buf_len=4096)

write_bytes = 'Hype boy yo!~'
last_time = time.ticks_ms()
read_data = 'Original'


try:
    while True:

        img = sensor.snapshot()         # Take a picture and return the image.
        
        if time.ticks_ms() - last_time > 500:
            last_time = time.ticks_ms()
            uart.write(write_bytes)
       
        
        if uart.any():
            read_data = uart.read()
            print("recv = ", read_data) 
            
          
        img.draw_string(2,200, read_data, color=(0, 176, 80), scale=2)
        lcd.display(img)              
       

except:
    pass
    
uart.deinit()
del uart
