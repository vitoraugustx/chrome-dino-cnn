import time
from PIL import Image
from mss import mss
import keyboard
import uuid
from pathlib import Path

"""
https://chrome.google.com/webstore/detail/online-dino/ckkofollclpnogccmelmlekkcgnanphc?hl=tr
"""

frame = {"top":300, "left":295, "width":360, "height":400} # Borders of the screenshot
ss_manager = mss()  # We are using mss() for taking a screenshot
count = 0           # A variable which count the screenshots
is_exit = False     # A variable for stopping the program


# A function for taking a screenshot
def take_screenshot(ss_id, key, path="./images/"):
    global count
    count += 1
    print("{}: {}".format(key, count))
    img = ss_manager.grab(frame)
    image = Image.frombytes("RGB", img.size, img.rgb)
    image.save(path +"{}_{}_{}.png".format(key, ss_id, count))
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

