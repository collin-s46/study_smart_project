from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from study_smart import db  # ✅ Import db only when needed

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    # Add relationship to tasks
    tasks = relationship('Task', backref='user', lazy=True)
    # Add relationship to events
    events = db.relationship('Event', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Values: major, minor, formative
    difficulty = db.Column(db.String(20), nullable=False)  # Values: hard, medium, easy
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    priority_score = db.Column(db.Integer, default=0)  # New field for priority score

    def calculate_priority_score(self):
        """
        Calculate the priority score based on task_type, difficulty, and due_date.
        """
        # Assign numerical values to task_type
        task_type_score = {
            'major': 3,
            'minor': 2,
            'formative': 1
        }.get(self.type, 0)  # Default to 0 if task_type is not recognized

        # Assign numerical values to difficulty
        difficulty_score = {
            'hard': 3,
            'medium': 2,
            'easy': 1
        }.get(self.difficulty, 0)  # Default to 0 if difficulty is not recognized

        # Calculate days until due date
        days_until_due = (self.due_date - date.today()).days
        due_date_score = max(0, 10 - days_until_due)  # Closer due date = higher score boost

        # Calculate total priority score
        self.priority_score = task_type_score + difficulty_score + due_date_score
        return self.priority_score

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

