import time
import cv2
import numpy as np

cam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
img_counter = 0
img_ratio = [0, 0]

while True:
    ret, frame = cam.read()
    img = cv2.flip(frame, 1)
    fmask = fgbg.apply(img)

    cv2.imshow("window", fmask)
    cv2.imshow("original", img)
    hi_gray = cv2.calcHist([fmask], [0], None, [3], [0, 256])

    img_counter += 1
    if (hi_gray[1] + hi_gray[2]) <= hi_gray[0] * 1.5 / 100:
        # print("No person")
        img_ratio[0] += 1
    else:
        # print("Yes person")
        img_ratio[1] += 1
    # print("{} {} {}".format(*hi_gray))
    # print(sum(hi_gray))

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

    if not ret:
        break
    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    cv2.imshow("test", h)

    # print(img_ratio)

    if img_counter == 5:
        img_counter = 0
        if img_ratio[0] > img_ratio[1]:
            # out.seek(0)
            out = open("out.txt", "w")
            out.write('0')
            out.close()
            print("No person")
            # print("{} {}".format(*img_ratio))
        else:
            # out.seek(0)
            out = open("out.txt", "w")
            out.write('1')
            out.close()
            print("Yes person")
            # print("{} {}".format(*img_ratio))
        img_ratio = [0, 0]
    time.sleep(1)

cam.release()
cv2.destroyAllWindows()