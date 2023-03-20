import tkinter
import customtkinter
import subprocess

import utils
import scrcpy
import cv2
from PIL import Image,ImageTk
import numpy as np
import time

adb = utils.AdbClient()

device_list = [d.serial for d in adb.device_list()]
device_clients=[]
device_view = []


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master,device_serial, **kwargs):
        super().__init__(master, **kwargs)
        self.device_serial = device_serial
        self.client = scrcpy.Client(device = device_serial,bitrate=1000,max_fps=24,max_width=480)

        self.client.start(threaded=True)
        device_clients.append(self.client)

        self.curret_image = customtkinter.CTkImage(dark_image=self.convert_frame(np.zeros([100,100,3],dtype=np.uint8)),size=self.client.resolution)
        
        self.image_view = customtkinter.CTkLabel(master = self, text=(device_serial), image=self.curret_image)
        self.image_view.grid(row=0, column=0)

        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)

        self.last_update = int( time.time() )

    # def update_clock(self):
    #     now = time.strftime("%H:%M:%S")
    #     self.label.configure(text=now)
    #     self.after(1000, self.update_clock)
    
    def convert_frame(self,frame):
        if frame is not None:
            img = frame[:, :, ::-1]
            return Image.fromarray(img)

    def on_frame(self,frame):
        now = int( time.time() )
        new_img = self.convert_frame(frame)
        if new_img is not None and  now - self.last_update>1/24:
            self.image_view.configure(image = customtkinter.CTkImage(dark_image=new_img,size=self.client.resolution))
            self.last_update = now
            # self.image_view.photo_ref = new_img

       


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # self.grid_rowconfigure(0, weight=1)  # configure grid system
        # self.grid_columnconfigure(0, weight=1)

        self.device_frames = [MyFrame(master=self,device_serial=d) for d in device_list]

        

        for index, frame in enumerate(self.device_frames):

            frame.grid(row=index, column=0, padx=5, pady=5, sticky="nsew")
    


app = App()

app.mainloop()

for client in device_clients:
    client.stop()
