import time
from playsound import playsound
import cv2

# Initializing image for alert
img = cv2.imread('bif_alert.bmp')
prev = -1

# Check the current state
while True:
    with open("out.txt", "r") as f:
        num = int(f.readline().strip())
        # If state changes
        if prev != num:
            # If state changes from 1 to 0
            if prev == 1:
                playsound("notscream.mp3")
                while True:
                    cv2.imshow("ALERT", img)
                    cv2.moveWindow("ALERT", 130, 50)
                    k = cv2.waitKey(0)
                    if k % 256 == 27:
                        cv2.destroyAllWindows()
                        break
            prev = num
    time.sleep(5)
