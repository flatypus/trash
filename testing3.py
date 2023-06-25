from time import time, sleep
import cv2
from skimage import metrics, measure
import numpy as np
import argparse
import matplotlib.pyplot as plt
import threading

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-v", "--video", required=True,
                        help="{int} for webcam")
args = vars(arg_parser.parse_args())
KERNEL_SIZE = 1


def diff(image1, image2):
    e1 = cv2.getTickCount()

    SHAPE = image1.shape
    KERNEL_SIZE = SHAPE[0] // 400

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

    _, thresh = cv2.threshold(closing, 200, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, None, iterations=1)
    thresh = cv2.dilate(thresh, None, iterations=20)

    e2 = cv2.getTickCount()
    time = (e2 - e1) / cv2.getTickFrequency()
    # print("Time taken : {} seconds".format(time))

    return thresh


def find_contours(image):
    # Find contours in thresh_gray after closing the gaps
    contours, hier = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def filter_contours(contours):
    return contours


def setup_camera(num):
    vid = cv2.VideoCapture(num)
    vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    return vid


def draw_target(draw_on, target):
    # smallest_c = sorted(contours, key=cv2.contourArea)[0]
    x, y, w, h = cv2.boundingRect(target)
    center_x, center_y = x+w//2, y+h//2
    with open(f"target_{args['video']}.txt", "a") as f:
        f.write(f"{center_x} {center_y} {time()}\n")
    cv2.rectangle(draw_on, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.circle(draw_on, (center_x, center_y), 50, (0, 0, 255), -1)


# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(
#     'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
url = None
try:
    url = int(args["video"])
except:
    url = args["video"]

with open(f"target_{args['video']}.txt", "w") as f:
    f.write("")
vid = setup_camera(url)

last_frame = None
last_contours = None
last_target = None

print("Started!!")
ret, frame = vid.read()
cv2.imshow('Frame', frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
    pass

sleep(20)

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
        last_contours = find_contours(diff(last_frame, frame))
        continue

    start_time = time()  # We would like to measure the FPS.
    difference = diff(last_frame, frame)

    draw_on = frame.copy()

    labels = measure.label(difference)
    mask = np.zeros(difference.shape, dtype="uint8")
    for label in np.unique(labels):
        if label == 0:
            continue
        labelMask = np.zeros(difference.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        if numPixels > 30:
            mask = cv2.add(mask, labelMask)

    contours = find_contours(mask)
    contours = filter_contours(contours)
    target = sorted(contours, key=cv2.contourArea)[0] if len(
        contours) > 0 else last_target
    if target is not None:
        draw_target(draw_on, target)
    # cv2.imshow("FRAME", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    last_frame = frame
    last_contours = contours
    last_target = target

    end_time = time()
    fps = 1/np.round(end_time - start_time, 3)  # Measure the FPS.
    # print(f"Frames Per Second : {fps}")

    # write fps
    cv2.putText(draw_on, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Frame', draw_on)
#
    ret, frame = vid.read()  # Read next frame.


# After the loop release the cap object
vid.release()
# vid2.release()
# Destroy all the windows
cv2.destroyAllWindows()
