from dotenv import load_dotenv
# from roboflow import Roboflow
from skimage import metrics, measure
from time import time, sleep
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from ultralytics import YOLO

load_dotenv()

# API_KEY = os.environ.get("API_KEY")
# MODEL_ENDPOINT = os.environ.get("MODEL_ENDPOINT")
# VERSION = 1
model = YOLO(
    "train5/weights/best.pt")

# rf = Roboflow(api_key=API_KEY)
# project = rf.workspace().project(MODEL_ENDPOINT)
# model = project.version(VERSION).model

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-v", "--video", required=True,
                        help="{int} for webcam")
args = vars(arg_parser.parse_args())


def find_ball(frame):
    results = model.predict(frame)
    return results[0].boxes.data


def setup_camera(num):
    vid = cv2.VideoCapture(num)
    vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    return vid


def draw_target(draw_on, target, last_target):
    # smallest_c = sorted(contours, key=cv2.contourArea)[0]
    if last_target is None:
        same = False
    else:
        same = target.tolist() == last_target.tolist()
    x, y, w, h = cv2.boundingRect(target)

    center_x, center_y = x+w//2, y+h//2
    with open(f"target_{args['video']}.txt", "a") as f:
        f.write(
            f"{center_x} {center_y} {time()}{' NEW' if (not same) else ''}\n")
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

# sleep(25)

while ret:
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    data = find_ball(frame)
    print(data)
    cv2.imshow('Frame', frame)

    ret, frame = vid.read()  # Read next frame.


# After the loop release the cap object
vid.release()
# vid2.release()
# Destroy all the windows
cv2.destroyAllWindows()
