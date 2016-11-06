
import json

from flask import Blueprint, render_template, request
from gevent import queue

from chat_room.model import User, Room

app = Blueprint('view', __name__)

rooms = {
    'topic1': Room(),
    'topic2': Room(),
}

users = {}


@app.route('/')
def choose_name():
    return render_template('choose.html')


@app.route('/<uid>')
def main(uid):
    return render_template('main.html',
                           uid=uid,
                           rooms=rooms.keys()
                           )


@app.route('/<room>/<uid>')
def join(room, uid):
    user = users.get(uid, None)

    if not user:
        users[uid] = user = User()

    active_room = rooms[room]
    active_room.subscribe(user)
    print('subscribe %s %s' % (active_room, user))

    messages = active_room.backlog()

    return render_template('room.html',
                           room=room, uid=uid, messages=messages)


@app.route("/put/<room>/<uid>", methods=["POST"])
def put(room, uid):
    user = users[uid]
    room = rooms[room]

    message = request.form['message']
    room.add(':'.join([uid, message]))

    return ''


@app.route("/poll/<uid>", methods=["POST"])
def poll(uid):
    try:
        msg = users[uid].queue.get(timeout=10)
    except queue.Empty:
        msg = []
    return json.dumps(msg)
