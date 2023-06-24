from time import time
import cv2
from skimage import metrics
import numpy as np
import matplotlib.pyplot as plt


def track(image1, image2):
    e1 = cv2.getTickCount()

    SHAPE = image1.shape
    KERNEL_SIZE = SHAPE[0] // 400

    # cv2.imshow('Frame', image1)

    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    # Compute SSIM between two images
    (score, diff) = metrics.structural_similarity(
        image1_gray, image2_gray, full=True)
    img = 255 - (diff * 255).astype("uint8")

    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    dilation = cv2.dilate(opening, kernel, iterations=40)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

    # Apply thresholding
    ret, thresh1 = cv2.threshold(closing, 50, 255, cv2.THRESH_BINARY)
    e2 = cv2.getTickCount()
    time = (e2 - e1) / cv2.getTickFrequency()
    print("Time taken : {} seconds".format(time))

    return thresh1


cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("Error opening video stream or file")


# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(
#     'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

lastframe = None

vid = cv2.VideoCapture(0)  # this is the magic!
vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


ret, frame = vid.read()
while ret:
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if lastframe is None:
        lastframe = frame
        continue

    start_time = time()  # We would like to measure the FPS.
    #  Perform tracking on the previous frame
    tracked = track(lastframe, frame)
    draw_on = frame.copy()
    # Update the lastframe with the current frame
    lastframe = frame

    contours, hier = cv2.findContours(
        tracked, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Draw the contours on the current frame
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(draw_on, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(draw_on, (x+w//2, y+h//2), 5, (0, 0, 255), -1)

    end_time = time()
    fps = 1/np.round(end_time - start_time, 3)  # Measure the FPS.
    print(f"Frames Per Second : {fps}")
    # write fps
    cv2.putText(draw_on, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Frame', draw_on)

    ret, frame = vid.read()  # Read next frame.

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
