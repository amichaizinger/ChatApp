from models import db, User, Message
from datetime import datetime

def add_user(username, avatar):
    new_user=User(username = username, avatar = avatar)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id


def add_message(sender_id, recipient_id, content):
    new_message=Message(sender_id = sender_id, recipient_id = recipient_id, content = content,
    timestamp = db.func.now())
    db.session.add(new_message)
    db.session.commit()
    return new_message.id

def get_chat_history(user1_id, user2_id):
    messages=Message.query.filter((Message.sender_id==user1_id) & (Message.recipient_id==user2_id)|
    (Message.sender_id==user2_id) & (Message.recipient_id==user1_id)).order_by(Message.timestamp).all()
    return [ #returns a list of message dictionary
        {"sender": message.sender_id, "recipient": message.recipient_id, "text": message.text, "time": message.timestamp}
        for message in messages
    ]


