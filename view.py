# image_viewer.py

import io
import os
import PySimpleGUI as sg
from PIL import Image
import adbutils
import scrcpy
import time
from utils import ADBInstance 

sg.theme('Dark Black 1')

adb = adbutils.AdbClient()

device_list = [d.serial for d in adb.device_list()]

client_list = []

### add script name

# scripts = ["YT SHORTS VIEW","YT CHANNEL VIEW"]

# def execute_script(script):
#     ###-ADD SCRIPT CONTENTS HERE-###
#     if(script==scripts[0]):
#         # for device in device_list:
#         #     d = ADBInstance(device)
#         #     d.open_Youtube()
#         #     # d.sleep(1)
#         #     d.tap(320,2280)
#         #     # d.sleep(2)
#         #     d.swipe(1080/2,1200,1080/2,600)
#         return


            

#     return

def main():
    layout = [
        # [sg.Text(f"Connected devices: {len(device_list)}"),[[sg.Text("Select script"),sg.Combo( scripts,key="-SELECT-SCRIPT-"),sg.Button("Run")]]],
        [[[sg.Text(device)],sg.Image(key=f"-DEVICE-{device}-")]for device in device_list],
    ]

    window = sg.Window("Device View", layout)

    for device in device_list:
        def convert_frame(frame):
            if frame is not None:
                
                img = frame[:, :, ::-1]
                return Image.fromarray(img)

        def on_frame(frame):
            new_img = convert_frame(frame)
            if new_img is not None:
                bio = io.BytesIO()
                convert_frame(frame).save(bio,format="PNG")
                try:
                    window[f"-DEVICE-{device}-"].update(bio.getvalue())
                except:
                    print(f"ERROR: {device}")

        client = scrcpy.Client(device=device,bitrate=1000,max_fps=24,max_width=480, stay_awake=True, lock_screen_orientation=0)
        client.start(threaded=True)
        client.add_listener(scrcpy.EVENT_FRAME, on_frame)
        client_list.append(client)




    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # if event=="Run":
        #     execute_script(values["-SELECT-SCRIPT-"])
            
        if callable(event):
            event()

    window.close()
    for client in client_list:
        client.stop()
    




if __name__ == "__main__":
    adb = adbutils.AdbClient()
    device_list = [d.serial for d in adb.device_list()]
    
    main()

