from aiohttp import web
import socketio
from collections import defaultdict

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

user_dict = {}
data_dict = defaultdict(list)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.on('bruh')
async def bruh(sid, data):
    print("bruh")


@sio.on('establish_user')
async def establish_user(sid, data):
    user_dict[sid] = data['user']
    print(user_dict)


@sio.on('ball_position')
async def ball_position(sid, data):
    data_dict[user_dict[sid]].append(data)
    print(f"User {user_dict[sid]}: {data}")


@sio.on('ping')
async def ping(sid, data):
    print("ping")
    await sio.emit('pong', data)


if __name__ == '__main__':
    PORT = 4000
    print(f'Serving on http://localhost:{PORT}')
    web.run_app(app, port=PORT)
