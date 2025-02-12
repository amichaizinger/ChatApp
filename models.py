from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    avatar = db.Column(db.String(200))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Sender
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Recipient
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    sender = db.relationship("User", foreign_keys=[sender_id])  # Get sender user
    recipient = db.relationship("User", foreign_keys=[recipient_id])  # Get recipient user