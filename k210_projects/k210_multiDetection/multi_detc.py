
import sensor, image, lcd, time
import KPU as kpu
from machine import UART
import gc, sys
from fpioa_manager import fm

input_size = (224, 224)
labels_obj = ['SS', 'SSS', 'SSSSS', 'P', 'A', 'AA', 'cherry', 'S', 'SSSS', 'PP', 'AAA', 'AAAA']
anchors_obj = [5.41, 3.88, 3.09, 1.97, 3.81, 2.56, 2.5, 1.56, 4.81, 3.06]
labels = ['rate', 'one', 'doubt', 'equal', 'nine', 'six', 'eight', 'zero', 'four', 'five', 'at', 'pound', 'two', 'three', 'seven']
anchors = [2.47, 1.38, 1.69, 1.72, 2.62, 2.19, 1.84, 1.0, 3.22, 1.84]


def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=input_size)
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

class Comm:
    def __init__(self, uart):
        self.uart = uart

    def send_detect_result(self, objects, labels):
        msg = ""
        for obj in objects:
            pos = obj.rect()
            p = obj.value()
            idx = obj.classid()
            label = labels[idx]
            msg += "{}:{}:{}:{}:{}:{:.2f}:{}, ".format(pos[0], pos[1], pos[2], pos[3], idx, p, label)
        if msg:
            msg = msg[:-2] + "\n"
        self.uart.write(msg.encode())

def init_uart():
    fm.register(8, fm.fpioa.UART1_TX)
    fm.register(6, fm.fpioa.UART1_RX)

    #uart = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)

    uart = UART(UART.UART1, 9600, read_buf_len=4096)
    return uart
def mode_number_detection(anchors, labels = None, model_addr="/sd/KPU/yolov2_classicSigns/ClassicSigns_v_2.kmodel", sensor_window=input_size, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):

    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    if not labels:
        with open('labels.txt','r') as f:
            exec(f.read())
    if not labels:
        print("no labels.txt")
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
        lcd.display(img)
        return 1
    try:
        img = image.Image("startup.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        lcd.display(img)

    uart = init_uart()
    #comm = Comm(uart)
    msg = "Loading..."
    last_time = time.ticks_ms()

    try:
        task = None
        task = kpu.load(model_addr)
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]
        while(True):
            img = sensor.snapshot()
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            t = time.ticks_ms() - t
            if objects:
                for obj in objects:
                    pos = obj.rect()
                    img.draw_rectangle(pos)
                    msg = "%s : %.2f" %(labels[obj.classid()], obj.value())
                    img.draw_string(pos[0], pos[1], msg, scale=2, color=(255, 105, 30))

            if time.ticks_ms() - last_time > 2700:
                last_time = time.ticks_ms()
                uart.write(msg+'~')
            lcd.display(img)
    except Exception as e:
        raise e
    finally:
        if not task is None:
            kpu.deinit(task)


def mode_objects_detection(anchors_obj, labels_obj = None, model_addr="/sd/KPU/yolov2_sign12/sign12.kmodel", sensor_window=input_size, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    if not labels_obj:
        with open('labels.txt','r') as f:
            exec(f.read())
    if not labels_obj:
        print("no labels.txt")
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
        lcd.display(img)
        return 1
    try:
        img = image.Image("startup.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        lcd.display(img)

    uart = init_uart()
    #comm = Comm(uart)
    msg = "Loading..."
    last_time = time.ticks_ms()

    try:
        task = None
        task = kpu.load(model_addr)
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors_obj) # threshold:[0,1], nms_value: [0, 1]
        while(True):


            img = sensor.snapshot()
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            t = time.ticks_ms() - t
            if objects:
                for obj in objects:
                    pos = obj.rect()
                    img.draw_rectangle(pos)
                    msg = "%s : %.2f" %(labels_obj[obj.classid()], obj.value())
                    img.draw_string(pos[0], pos[1], msg, scale=2, color=(255, 105, 30))

            if time.ticks_ms() - last_time > 2500:
                last_time = time.ticks_ms()
                uart.write(msg+'~')
                #comm.send_detect_result(objects, labels)

            lcd.display(img)
    except Exception as e:
        raise e
    finally:
        if not task is None:
            kpu.deinit(task)


def mode_barQRcodes_detection():

    clock = time.clock()
    lcd.init()
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_vflip(1)
    sensor.run(1)
    sensor.skip_frames(30)
    sensor.set_hmirror(1)

    uart = init_uart()

    write_bytes = 'Loading...'
    last_time = time.ticks_ms()

    try:
        while (True):

            clock.tick()
            img = sensor.snapshot()


            for i in img.find_barcodes():
                img.draw_string(int(i.rect()[0]),int(i.rect()[1]), i.payload(), color=(10,200,250), scale=2)
                img.draw_rectangle(i.rect(), color=(10,200,250),thickness = 2)
                if time.ticks_ms() - last_time > 2500:
                    last_time = time.ticks_ms()
                    uart.write('%s~'%(i.payload()))

            for i in img.find_qrcodes():
                img.draw_string(int(i.rect()[0]),int(i.rect()[1]), i.payload(), color=(250,200,10), scale=2)
                img.draw_rectangle(i.rect(), color=(250,200,10),thickness = 2)
                if time.ticks_ms() - last_time > 2500:
                    last_time = time.ticks_ms()
                    uart.write('%s~'%(i.payload()))

            lcd.display(img)                # Display image on lcd.


    except:
        pass
    uart.deinit()



def main():

    lcd.init(freq=20000000)
    uart = init_uart()

    mode = 0
    pret = time.ticks_ms()
    while time.ticks_ms() - pret < 10000:

        img = image.Image(size=(320, 240))
        img.draw_string(3, 3, "Select Mode: ", color=(10, 50, 200), scale=2)
        img.draw_string(3, 45, "1. Digit", color=(10, 50, 200), scale=2)
        img.draw_string(3, 85, "2. Object", color=(10, 50, 200), scale=2)
        img.draw_string(3, 125, "3. bar&QR", color=(10, 50, 200), scale=2)

        if uart.any():
            mode = int(uart.read().decode('utf-8'))
        img.draw_string(150, 3, "%d" % mode, color=(210, 210, 210), scale=2)

        lcd.display(img)


    while True:

        if uart.any():
            data = uart.read()
            if data:
                try:
                    mode = int(data.strip())
                except ValueError:
                    continue
        if mode == 1:
            print(mode)
            mode_number_detection(anchors = anchors, labels=labels, model_addr="/sd/KPU/yolov2_classicSigns/ClassicSigns_v_2.kmodel")

        elif mode == 2:
            mode_objects_detection(anchors_obj, labels_obj, model_addr="/sd/KPU/yolov2_sign12/sign12.kmodel", sensor_window=input_size, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False)

        elif mode == 3:
            mode_barQRcodes_detection()
        else:
            img = image.Image(size=(320, 240))
            img.draw_string(3, 3, "Select Mode: ", color=(10, 50, 200), scale=2)
            img.draw_string(3, 45, "1. Digit", color=(10, 50, 200), scale=2)
            img.draw_string(3, 85, "2. Object", color=(10, 50, 200), scale=2)
            img.draw_string(3, 125, "3. bar&QR", color=(10, 50, 200), scale=2)
            lcd.display(img)





if __name__ == "__main__":
    try:

        main()
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
