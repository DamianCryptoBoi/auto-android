from utils import adb
import scrcpy
import cv2

adb.connect("127.0.0.1:5555")

client = scrcpy.Client(device=adb.device_list()[0],bitrate=100,max_fps=10,max_width=480)

def on_frame(frame):
    # If you set non-blocking (default) in constructor, the frame event receiver 
    # may receive None to avoid blocking event.
    if frame is not None:
        # frame is an bgr numpy ndarray (cv2' default format)
        cv2.imshow(adb.device_list()[0].serial, frame)
    cv2.waitKey(10)
        # print(frame)

client.add_listener(scrcpy.EVENT_FRAME, on_frame)

client.start(threaded=True)


