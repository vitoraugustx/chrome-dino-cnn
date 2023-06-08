import time
from PIL import Image
from mss import mss
import keyboard
import uuid
from pathlib import Path
import cv2
import numpy as np

"""
https://chrome.google.com/webstore/detail/online-dino/ckkofollclpnogccmelmlekkcgnanphc?hl=tr
"""

# bounding boxes
# [x, y, width, height]
x, y, w, h = 230, 350, 360, 360
bboxes = [np.array([x, y, w, h])]
frame = {"top":0, "left":0, "width":1920, "height":1080} # Borders of the screenshot
roi_frame = {"top": y, "left": x, "width": w, "height": h} # Borders of the region of interest

ss_manager = mss()  # We are using mss() for taking a screenshot
count = 0           # A variable which count the screenshots
is_exit = False     # A variable for stopping the program

def draw_bboxes(img, bboxes, color=(0, 0, 255), thickness=2):
    for bbox in bboxes:
        cv2.rectangle(img, tuple(bbox[:2]), tuple(bbox[:2]+bbox[-2:]), color, thickness)

# A function for taking a screenshot
def take_screenshot(ss_id, key, path="./images/"):
    global count
    count += 1
    print("{}: {}".format(key, count))
    roi = ss_manager.grab(roi_frame)
    img = ss_manager.grab(frame)

    image = Image.frombytes("RGB", roi.size, roi.rgb)
    image.save(path +"{}_{}_{}.png".format(key, ss_id, count))
    
    screen = np.asarray(img)
    # convert from BGRA --> BGR
    screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
    draw_bboxes(screen, bboxes)
    resized = cv2.resize(screen, (1366, 768))
    # display
    cv2.imshow("OpenCV/Numpy normal", resized)
    cv2.waitKey()
    time.sleep(1.5)


# A function for stopping the program
def exit():
    global is_exit
    is_exit = True


# MAIN PROGRAM
if __name__ == '__main__':
    Path("./images/").mkdir(parents=True, exist_ok=True) # Create images directory if not exist
    Path("./images/up").mkdir(parents=True, exist_ok=True) # Create images directory if not exist
    Path("./images/down").mkdir(parents=True, exist_ok=True) # Create images directory if not exist
    Path("./images/none").mkdir(parents=True, exist_ok=True) # Create images directory if not exist
    keyboard.add_hotkey("esc", exit)    # If user clik the 'esc', the program will stop
    ss_id = uuid.uuid4()                # An id for all screenshots

    while True: # An infinite loop for taking screenshot until user stop the program
        if is_exit == True: 
            break

        try:
            if keyboard.is_pressed(keyboard.KEY_UP):        # If 'up' key is pressed
                take_screenshot(ss_id, "up", path="./images/up/")
                time.sleep(0.01)
            elif keyboard.is_pressed(keyboard.KEY_DOWN):    # If 'down' key is pressed
                take_screenshot(ss_id, "down", path="./images/down/")
                time.sleep(0.01)
            elif keyboard.is_pressed("right"):              # If 'right' key is pressed
                take_screenshot(ss_id, "right", path="./images/none/")
                time.sleep(0.01)
        except RuntimeError: 
            continue

