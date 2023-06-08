import cv2
import time
import numpy as np
from mss import mss

def draw_bboxes(img, bboxes, color=(0, 0, 255), thickness=2):
    for bbox in bboxes:
        return cv2.rectangle(img, tuple(bbox[:2]), tuple(bbox[:2]+bbox[-2:]), color, thickness)

# bounding boxes
bboxes = [np.array([300, 295, 360, 400])]

with mss() as sct:
    # part of the screen to capture
    monitor = {"top":0, "left":0, "width":1920, "height":1080}
    
    # get screen
    screen = np.asarray(sct.grab(monitor))
    
    # convert from BGRA --> BGR
    screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
    # draw bboxes
    screen = draw_bboxes(screen, bboxes)
    resized = cv2.resize(screen, (1366, 768))

    # display
    cv2.imshow("OpenCV/Numpy normal", resized)
    cv2.waitKey()
    
        
   