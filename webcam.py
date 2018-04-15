import time
import cv2
import numpy as np

# Initializing camera, mask and windows
cam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
cv2.namedWindow("Original")
cv2.moveWindow("Original", 0, 0)
cv2.namedWindow("Masked")
cv2.moveWindow("Masked", 640, 0)
cv2.namedWindow("Histogram")
cv2.moveWindow("Histogram", 480, 350)
font = cv2.cv2.FONT_HERSHEY_SIMPLEX


# Initializing counters for b/w ratio
img_counter = 0
img_ratio = [0, 0]

while True:
    # Reading frame from camera and applying the mask
    ret, frame = cam.read()
    img = cv2.flip(frame, 1)
    fmask = fgbg.apply(img)

    if not ret:
        break

    # 2D histogram for original colored image
    h = np.zeros((300, 256, 3))

    bins = np.arange(256).reshape(256, 1)
    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([img], [ch], None, [256], [0, 255])
        cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_item))
        pts = np.column_stack((bins, hist))
        cv2.polylines(h, [pts], False, col)

    h = np.flipud(h)

    # 1D histogram for masked image
    hi_gray = cv2.calcHist([fmask], [0], None, [3], [0, 256])

    # Checking whether the 3/5 images were black or white
    img_counter += 1
    if (hi_gray[1] + hi_gray[2]) <= hi_gray[0] * 1.5 / 100:
        # If black
        cv2.putText(fmask, "No person", (0, 45), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
        img_ratio[0] += 1
    else:
        # If white
        cv2.putText(fmask, "Yes person", (0, 45), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
        img_ratio[1] += 1

    # print("{} {} {}".format(*hi_gray))

    # Showing frames and histogram
    cv2.imshow("Original", img)
    cv2.imshow("Masked", fmask)
    cv2.imshow("Histogram", h)

    # Writing current state to a file
    if img_counter == 5:
        img_counter = 0
        if img_ratio[0] > img_ratio[1]:
            with open("out.txt", "w") as f:
                f.write('0 1')
            print("No person")
        else:
            with open("out.txt", "w") as f:
                f.write('1 1')
            print("Yes person")
        img_ratio = [0, 0]

    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    time.sleep(1)

with open("out.txt", "w") as f:
    f.write('1 0')
cam.release()
cv2.destroyAllWindows()
