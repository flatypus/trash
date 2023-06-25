from time import time
import cv2
from skimage import metrics
import numpy as np
import argparse
import matplotlib.pyplot as plt
import threading

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-v", "--video", required=True,
                        help="{int} for webcam")
args = vars(arg_parser.parse_args())


def track(image1, image2):
    e1 = cv2.getTickCount()

    # SHAPE = image1.shape
    KERNEL_SIZE = 1

    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

    lower_green = np.array([30, 82, 40])
    upper_green = np.array([140, 229, 204])

    mask1 = cv2.inRange(hsv1, lower_green, upper_green)
    mask2 = cv2.inRange(hsv2, lower_green, upper_green)

    cv2.imshow('Frame', mask1)
    cv2.imshow('Image', image1)

    # Compute SSIM between two images
    (score, diff) = metrics.structural_similarity(
        mask1, mask2, full=True)

    img = 255 - (diff * 255).astype("uint8")

    cv2.imshow('Frame', img)

    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    frame = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    frame = cv2.dilate(frame, kernel, iterations=40)
    closing = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

    # Apply thresholding
    ret, thresh1 = cv2.threshold(closing, 50, 255, cv2.THRESH_BINARY)

    cv2.imshow('Frame', thresh1)
    # cv2.imshow('Frame', thresh1)
    e2 = cv2.getTickCount()
    time = (e2 - e1) / cv2.getTickFrequency()
    print("Time taken : {} seconds".format(time))

    return thresh1


def find_contours(image):
    # Find contours in thresh_gray after closing the gaps
    contours, hier = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def filter_contours(contours):
    if len(contours) == 0:
        return contours
    # filter small
    contours = [c for c in contours if cv2.contourArea(c) > 1000]
    # filter big
    contours = [c for c in contours if cv2.contourArea(c) < 100000]
    return contours


def setup_camera(num):
    vid = cv2.VideoCapture(num)
    vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    return vid


def draw_contours(image, contours, last_contours):
    # Draw the contours on the current frame
    for c in contours:
        keep_contour = False
        previous_contour = None
        smallest_distance = 1000000000000
        for last_c in last_contours:
            # check bounding box overlap
            x, y, w, h = cv2.boundingRect(c)
            last_x, last_y, last_w, last_h = cv2.boundingRect(last_c)
            center = (x + w//2, y + h//2)
            last_center = (last_x + last_w//2, last_y + last_h//2)
            distance = np.linalg.norm(
                np.array(center) - np.array(last_center))
            if distance < smallest_distance:
                smallest_distance = distance
                previous_contour = last_c
                keep_contour = True

        if not keep_contour:
            continue

        x, y, w, h = cv2.boundingRect(c)
        contour_center = (x + w//2, y + h//2)
        last_x, last_y, last_w, last_h = cv2.boundingRect(previous_contour)
        previous_contour_center = (last_x + last_w//2, last_y + last_h//2)
        # draw contour itself
        # cv2.drawContours(draw_on, [c], -1, (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(image, contour_center, 5, (0, 0, 255), -1)
        # draw line from previous contour center to current contour center
        cv2.line(image, previous_contour_center,
                 contour_center, (0, 0, 255), 2)


# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(
#     'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
url = None
try:
    url = int(args["video"])
except:
    url = args["video"]

vid = setup_camera(url)

last_frame = None
last_contours = None
ret, frame = vid.read()

while ret:
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if last_frame is None:
        last_frame = frame
        continue

    if last_contours is None:
        last_contours = find_contours(track(last_frame, frame))
        continue

    start_time = time()  # We would like to measure the FPS.
    #  Perform tracking on the previous frame
    tracked = track(last_frame, frame)
    contours = find_contours(tracked)
    contours = filter_contours(contours)

    draw_on = frame.copy()
    draw_contours(draw_on, contours, last_contours)

    # Update the previous frame and previous points
    last_frame = frame
    last_contours = contours

    end_time = time()
    fps = 1/np.round(end_time - start_time, 3)  # Measure the FPS.
    print(f"Frames Per Second : {fps}")

    # write fps
    cv2.putText(draw_on, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # cv2.imshow('Frame', draw_on)

    ret, frame = vid.read()  # Read next frame.

# After the loop release the cap object
vid.release()
# vid2.release()
# Destroy all the windows
cv2.destroyAllWindows()
