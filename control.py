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

scripts = ["YT SHORTS VIEW","YT CHANNEL VIEW"]

def execute_script(script):
    ###-ADD SCRIPT CONTENTS HERE-###
    if(script==scripts[0]):
        for device in device_list:
            # d = ADBInstance(device)
            # d.open_Youtube()
            # d.sleep(2)
            # d.tap(320,2280)
            # d.sleep(2)
            # d.swipe(1080/2,1200,1080/2,600)
            return

def main():
    layout = [
        [sg.Text(f"Connected devices: {len(device_list)}"),[[sg.Text("Select script"),sg.Combo( scripts,key="-SELECT-SCRIPT-"),sg.Button("Run")]]]
    ]

    window = sg.Window("Control Center", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event=="Run":
            execute_script(values["-SELECT-SCRIPT-"])
            break
            
        if callable(event):
            event()

    window.close()
    for client in client_list:
        client.stop()
    




if __name__ == "__main__":
    adb = adbutils.AdbClient()
    device_list = [d.serial for d in adb.device_list()]
    
    main()

