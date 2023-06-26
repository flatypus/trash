import asyncio
import socketio
import argparse
import cv2
import numpy as np
from dotenv import load_dotenv
from time import time, sleep
from ultralytics import YOLO


sio = socketio.AsyncClient()


@sio.event
async def connect():
    print('connection established')
    await sio.emit('establish_user', {'user': 1})


@sio.event
async def disconnect():
    print('disconnected from server')


class Color():
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


load_dotenv()

model = YOLO("yolov8_model/weights/best.pt")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-v", "--video", required=True,
                        help="{int} for webcam")
arg_parser.add_argument("-plot", "--plot", required=False,
                        help="plot the data")
args = vars(arg_parser.parse_args())
should_plot = args["plot"] is not None


class Timer():
    def __init__(self):
        self.start_time = time()

    def reset(self):
        self.start_time = time()

    def elapsed(self):
        return time() - self.start_time


class Tracker():
    def find_ball(self, frame):
        results = model.predict(frame, device="mps", verbose=False)
        return results[0].boxes

    def setup_camera(self, num):
        vid = cv2.VideoCapture(num)
        vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        return vid

    def draw_target(self, target):
        (x, y, x2, y2) = target
        draw_on = self.frame
        center_x, center_y = int((x+x2)/2), int((y+y2)/2)

        with open(f"target_{args['video']}.txt", "w" if should_plot else "a") as f:
            f.write(
                f"{center_x} {center_y} {time()}{' NEW' if (target != self.last_target) else ''}\n")

        cv2.rectangle(draw_on, (x, y), (x2, y2), Color.GREEN, 2)
        cv2.circle(draw_on, (center_x, center_y), 5, Color.RED, -1)

        if self.last_target is not None:
            (last_x, last_y, last_x2, last_y2) = self.last_target
            last_center_x, last_center_y = int(
                (last_x+last_x2)/2), int((last_y+last_y2)/2)
            cv2.circle(draw_on, (center_x, center_y), 5, Color.BLUE, -1)
            cv2.line(draw_on, (last_center_x, last_center_y),
                     (center_x, center_y), Color.BLUE, 2)

    def track(self):
        self.timer.reset()
        data = self.find_ball(self.frame)
        bboxes = np.array(data.xyxy.cpu(), dtype="int").tolist()

        if len(bboxes) > 0:
            target = bboxes[0]
            self.draw_target(target)
            self.last_target = target

            # Emit the ball position to the server
            center_x, center_y = int(
                (target[0]+target[2])/2), int((target[1]+target[3])/2)
            print(f"({center_x}, {center_y})")
            sio.emit('ball_position', {'x': center_x, 'y': center_y})

        elapsed = self.timer.elapsed()
        fps = 1/np.round(elapsed, 3)
        self.timer.reset()

        cv2.putText(self.frame, f"FPS: {fps}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, Color.RED, 2)

    def ping_in_intervals(self):
        while True:
            asyncio.run(sio.emit('ping'))
            sleep(1)

    def __init__(self):
        self.timer = Timer()

        url = None
        try:
            url = int(args["video"])
        except:
            url = args["video"]

        with open(f"target_{args['video']}.txt", "w") as f:
            f.write("")
        self.vid = self.setup_camera(url)

        self.last_target = None

        print("Started!!")

        self.ret, self.frame = self.vid.read()
        # sio.start_background_task(self.ping)
        thread = sio.start_background_task(self.ping_in_intervals)
        # Establish connection to the server

        while self.ret:
            self.track()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imshow('Frame', self.frame)
            self.ret, self.frame = self.vid.read()

        self.vid.release()
        cv2.destroyAllWindows()
        asyncio.run(sio.disconnect())


if __name__ == "__main__":
    asyncio.run(sio.connect('http://localhost:4000'))
    asyncio.run(Tracker())
