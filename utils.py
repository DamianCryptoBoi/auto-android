from adbutils import adb

class ADBInstance:
    def __init__(self, device_serial):
        self.device_serial = device_serial
        self.instance = adb.device(serial = device_serial)
    
    def sleep(self,seconds):
        self.instance.shell(f"sleep {seconds}")

    def open_Youtube(self):
        self.instance.shell("monkey -p com.google.android.youtube 1")

    def tap(self,x,y):
        self.instance.shell(f"input tap {x} {y}")

    def swipe(self, x1,y1,x2,y2):
        self.instance.shell(f"inpur tap {x1} {y1} {x2} {y2} 200")


    