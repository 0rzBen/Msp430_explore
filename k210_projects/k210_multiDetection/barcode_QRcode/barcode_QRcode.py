import sensor, image, time, math,lcd


lcd.init(freq=20000000)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
# sensor.set_framesize(sensor.QVGA) # High Res!
# sensor.set_windowing((640, 80)) # V Res of 80 == less work (40 for 2X the speed).
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()              # Create a clock object to track the FPS.

# binding UART1 IO:6->RX, 8->TX  //UART2 contradicts the sensor when communicating with msp430f5529
from fpioa_manager import fm
from machine import UART
fm.register(6, fm.fpioa.UART1_RX)
fm.register(8, fm.fpioa.UART1_TX)
yb_uart = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)



write_bytes = b'Loading...~'
last_time = time.ticks_ms()


def barcode_name(code):
    if(code.type() == image.EAN2):
        return "EAN2"
    if(code.type() == image.EAN5):
        return "EAN5"
    if(code.type() == image.EAN8):
        return "EAN8"
    if(code.type() == image.UPCE):
        return "UPCE"
    if(code.type() == image.ISBN10):
        return "ISBN10"
    if(code.type() == image.UPCA):
        return "UPCA"
    if(code.type() == image.EAN13):
        return "EAN13"
    if(code.type() == image.ISBN13):
        return "ISBN13"
    if(code.type() == image.I25):
        return "I25"
    if(code.type() == image.DATABAR):
        return "DATABAR"
    if(code.type() == image.DATABAR_EXP):
        return "DATABAR_EXP"
    if(code.type() == image.CODABAR):
        return "CODABAR"
    if(code.type() == image.CODE39):
        return "CODE39"
    if(code.type() == image.PDF417):
        return "PDF417"
    if(code.type() == image.CODE93):
        return "CODE93"
    if(code.type() == image.CODE128):
        return "CODE128"
        
        
try:
    while True:

        clock.tick()
        img = sensor.snapshot()
     
        for code in img.find_barcodes():
            x,y,w,h = code.rect()
            img.draw_rectangle(code.rect(),color=(255, 255, 255))
        
            print_args = (barcode_name(code), code.payload(), (180 * code.rotation()) / math.pi, code.quality(), clock.fps())
            print("Barcode %s, Payload \"%s\", rotation %f (degrees), quality %d, FPS %f" % print_args)
            img.draw_string(x,y, code.payload(), color=(255, 255, 255), scale=2)
            if time.ticks_ms() - last_time > 2500:
                last_time = time.ticks_ms()
                yb_uart.write(b'%s~'%(code.payload()))
                
        for code in img.find_qrcodes():
            img.draw_rectangle(code.rect(), color = 127, thickness=3)
            img.draw_string(code.x(),code.y()-20,code.payload(),color=(255,255,255),scale=2)
            print(code)
            if time.ticks_ms() - last_time > 2500:
                last_time = time.ticks_ms()
                yb_uart.write(b'%s~'%(code.payload()))

        
        # read and print data
        
        '''
        if yb_uart.any():
            read_data = yb_uart.read()
            if read_data:
               img.draw_string(2,2, read_data, color=(0, 176, 80), scale=2)
               tmp = read_data
               print(read_data)
        '''
       
        lcd.display(img)                # Display image on lcd.


except:
    pass

yb_uart.deinit()
del yb_uart