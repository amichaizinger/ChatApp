from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"  # SQLite database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
socketio = SocketIO()

db.init_app(app)
socketio.init_app(app)

usernum=1000
users = {}  # Key: socket_id, Value: {"username": ..., "avatar": ...}
rooms = {}  # Key: room_name, Value: List of socket_ids


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on("connect")
def handel_connect(usernum):
    usernum+=1
    username='username_''usernum'
    avatar='img.png'
    users[request.sid]={'username':username, 'avatar': avatar}

@socketio.on("send_message")
def handle_message(data):
    sender = users.get(request.sid, None)
    recipient_username = data.get("recipient", None)  # If None, it's a public message

    if sender is not None:
        message_data = {
            "username": sender["username"],
            "avatar": sender["avatar"],
            "message": data["message"]
        }

        if recipient_username is not None:  # Private Message
            recipient_sid = None
            for sid, user in users.items():
                if user["username"] == recipient_username:
                    recipient_sid = sid
                    break  # Stop once we find the first match
            if recipient_sid is not None:
                emit("new_message", message_data, room=recipient_sid)  # Send only to recipient
        else:  # Public Message
            emit("new_message", message_data, broadcast=True)


@socketio.on("update_username")
def Update_Username(data):
    users[request.sid]["username"] = data["username"]

if __name__=="__main__":
    socketio.run(app)
