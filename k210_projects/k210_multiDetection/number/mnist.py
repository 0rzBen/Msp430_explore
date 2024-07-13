import sensor, image, time, lcd
from maix import KPU
import gc


lcd.init(freq=20000000)                          # Init lcd display

sensor.reset()                      # Reset and initialize the sensor. It will

sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.set_windowing((224, 224))
sensor.skip_frames(time = 1000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

kpu = KPU()
kpu.load_kmodel("/sd/KPU/mnist/uint8_mnist_cnn_model.kmodel")


# binding UART1 IO:6->RX, 8->TX  //UART2 contradicts the sensor when communicate with msp430f5529
from fpioa_manager import fm
from machine import UART
fm.register(6, fm.fpioa.UART1_RX)
fm.register(8, fm.fpioa.UART1_TX)
yb_uart = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)


last_time = time.ticks_ms()
write_bytes = b'Loading...~'

try:
    while True:

        if time.ticks_ms() - last_time > 500:
            last_time = time.ticks_ms()
            yb_uart.write(write_bytes)

        gc.collect()
        img = sensor.snapshot()
        img_mnist1=img.to_grayscale(1)        #convert to gray
        img_mnist2=img_mnist1.resize(112,112)
        a=img_mnist2.invert()                 #invert picture as mnist need
        a=img_mnist2.strech_char(1)           #preprocessing pictures, eliminate dark corner
        a=img_mnist2.pix_to_ai()

        out = kpu.run_with_output(img_mnist2, getlist=True)
        max_mnist = max(out)
        index_mnist = out.index(max_mnist)
        #score = KPU.sigmoid(max_mnist)
        display_str = "num: %d" % index_mnist
        write_bytes = b"num: %d~" % index_mnist
        print(display_str)


        # read and print data

        '''
        if yb_uart.any():
            read_data = yb_uart.read()
            if read_data:
               img.draw_string(70,160, read_data, color=(0, 176, 80), scale=2)
               tmp = read_data
               print(read_data)

        '''
        a=img.draw_string(4,3,display_str,color=(20,50,200),scale=2)
        lcd.display(img)                # Display image on lcd.


except:
    pass

yb_uart.deinit()
kpu.deinit()
