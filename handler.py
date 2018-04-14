import time
from playsound import playsound
import cv2


img = cv2.imread('bif_alert.bmp')
prev = -1
while True:
    with open("out.txt", "r") as f:
        num = int(f.readline().strip())
        if prev!=num:
            if prev == 1:
                playsound("notscream.mp3")
                cv2.moveWindow("ALERT", 100, 100)
                while True:
                    cv2.imshow("ALERT", img)

                    k = cv2.waitKey(1)
                    if k % 256 == 27:
                        cv2.destroyAllWindows()
                        break
            prev = num
    time.sleep(5)
