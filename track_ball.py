from dotenv import load_dotenv
from time import time, sleep
from ultralytics import YOLO
import argparse
import cv2
import numpy as np

# color enums


class Color():
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


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
arg_parser.add_argument("-plot", "--plot", required=False,
                        help="plot the data")
args = vars(arg_parser.parse_args())
should_plot = args["plot"] is not None


def find_ball(frame):
    results = model.predict(frame, device="mps", verbose=False)
    return results[0].boxes


def setup_camera(num):
    vid = cv2.VideoCapture(num)
    vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    return vid


def draw_target(draw_on, target, last_target):
    (x, y, x2, y2) = target
    center_x, center_y = int((x+x2)/2), int((y+y2)/2)

    with open(f"target_{args['video']}.txt", "w" if should_plot else "a") as f:
        f.write(
            f"{center_x} {center_y} {time()}{' NEW' if (target != last_target) else ''}\n")

    cv2.rectangle(draw_on, (x, y), (x2, y2), Color.GREEN, 2)
    cv2.circle(draw_on, (center_x, center_y), 5, Color.RED, -1)

    if last_target is not None:
        (last_x, last_y, last_x2, last_y2) = last_target
        last_center_x, last_center_y = int(
            (last_x+last_x2)/2), int((last_y+last_y2)/2)
        cv2.circle(draw_on, (center_x, center_y), 5, Color.BLUE, -1)
        # drae trailing line from last target to current target
        cv2.line(draw_on, (last_center_x, last_center_y),
                 (center_x, center_y), Color.BLUE, 2)


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

last_target = None

print("Started!!")
ret, frame = vid.read()


# ONLY UNCOMMENT THIS TO SETUP FOR RECORDING
# cv2.imshow('Frame', frame)


if cv2.waitKey(1) & 0xFF == ord('q'):
    pass


# ONLY UNCOMMENT THIS TO SETUP FOR RECORDING
# sleep(20)
wait = time()

while ret:
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    start_time = time()
    data = find_ball(frame)
    bboxes = np.array(data.xyxy.cpu(), dtype="int").tolist()

    if len(bboxes) > 0:
        target = bboxes[0]
        # print(f"Target bounding box: {target}")
        draw_target(frame, target, last_target)
        last_target = target

    end_time = time()
    fps = 1/np.round(end_time - start_time, 3)  # Measure the FPS.

    # write fps
    cv2.putText(frame, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, Color.RED, 2)

    cv2.imshow('Frame', frame)

    # if time() - wait > 12:
    #     break

    ret, frame = vid.read()  # Read next frame.

# After the loop release the cap object
vid.release()
# vid2.release()
# Destroy all the windows
cv2.destroyAllWindows()
