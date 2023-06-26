import cv2
import asyncio
import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print('connection established')
    await sio.emit('establish_user', {'user': 1})


@sio.event
async def disconnect():
    print('disconnected from server')


async def main():
    await sio.connect('http://localhost:4000')
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())


def setup_camera(num):
    vid = cv2.VideoCapture(num)
    vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    return vid


video_stream = 0

vid = setup_camera(video_stream)
ret, frame = vid.read()
while ret:

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    object_points = []
    image_points = []

    # intrinsic_params = cv2.calibrateCamera()
    extrinsic_params = cv2.solvePnP()
    print(extrinsic_params)
    cv2.imshow('Frame', frame)
    ret, frame = vid.read()

vid.release()
cv2.destroyAllWindows()
