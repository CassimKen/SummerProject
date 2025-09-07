from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lessons = db.relationship('Lesson', backref='coach', lazy=True)

class Learner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    emergency_contact = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    grade = db.Column(db.Integer) 
    bookings = db.relationship('Booking', backref='learner', lazy=True)
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20)) 
    time = db.Column(db.String(20))  
    grade = db.Column(db.Integer)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'))
    bookings = db.relationship('Booking', backref='lesson', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('learner.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    status = db.Column(db.String(10))  
    review = db.Column(db.String(500))
    rating = db.Column(db.Integer) 
