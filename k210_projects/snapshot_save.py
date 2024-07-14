# Snapshot Example
#
# Note: You will need an SD card to run this example.
#
# You can use your CanMV Cam to save image files.

import sensor, time, image, gc, sys    # 导入感光元件模块 sensor 跟踪运行时间模块 time 机器视觉模块 image
from fpioa_manager import fm       # 从 fpioa_manager 模块中导入 引脚注册模块 fm
from Maix import GPIO              # 从 Maix 模块中导入 模块 GPIO
import lcd    

fm.register(27, fm.fpioa.GPIO2, force = True)               #  LED_R 
fm.register(26, fm.fpioa.GPIO1, force = True)               #  LED_G 
fm.register(29, fm.fpioa.GPIO0, force = True)               #  LED_B 

# 创建 LED 对象
LED_R = GPIO(GPIO.GPIO2, GPIO.OUT)                          # 创建 LED_R 对象
LED_G = GPIO(GPIO.GPIO1, GPIO.OUT)                          # 创建 LED_G 对象
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT)                          # 创建 LED_B 对象

'''红灯常亮
LED_R.value(0)
LED_G.value(1)
LED_B.value(1)
'''

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(False)
sensor.set_vflip(False)
sensor.run(1)
lcd.init(type=1)
lcd.rotation(0)
lcd.clear(lcd.WHITE)


last_time = time.ticks_ms()

#Prepare...
while(time.ticks_ms() - last_time < 5000):
    LED_R.value(0)
    LED_G.value(1)
    LED_B.value(1)
    
    img = sensor.snapshot()
    lcd.display(img)
    
last_time = time.ticks_ms()

LED_R.value(1)
LED_G.value(1)
LED_B.value(1)

cnt = 0

while(1):
    img = sensor.snapshot()
    
    
    if time.ticks_ms() - last_time > 100:
        cnt += 1
        print("num:%d" % cnt)
        last_time = time.ticks_ms()
        sensor.snapshot().save("/sd/sign12/P/P_%d.jpg" % cnt) # or "example.bmp" (or others)
            
    img.draw_string(4,3, "num:%d"%cnt, color = (0, 0, 0), scale = 2)        
    lcd.display(img)
    if cnt == 250:
        break
        
LED_R.value(1)
LED_G.value(0)
LED_B.value(1)
print("Done! Reset the camera to see the saved image.")
