import cv2
from skimage import metrics
import numpy as np
import matplotlib.pyplot as plt


def track(image1, image2):
    e1 = cv2.getTickCount()

    SHAPE = image1.shape
    KERNEL_SIZE = SHAPE[0] // 400

    cv2.imshow('Frame', image1)

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


cap = cv2.VideoCapture('small.mov')

if (cap.isOpened() == False):
    print("Error opening video stream or file")


frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

lastframe = None

# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        if lastframe is None:
            lastframe = frame
            continue
        # Perform tracking on the previous frame
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

        # Display the resulting frame
        cv2.imshow('Frame', draw_on)
        out.write(draw_on)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the video capture object
out.release()
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
