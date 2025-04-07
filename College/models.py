from College import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),default='default.jpg', nullable=False)
    password = db.Column(db.String(60), nullable=False)
    feedbacks = db.relationship('Feedback', backref='author', lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.phone}','{self.feedback}')"
    

class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    signature = db.Column(db.String(200), nullable=False)
    current_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)




class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)  # Store as string or text for simplicity
    class_name = db.Column(db.String(50), nullable=False)
    admission_date = db.Column(db.String(20), nullable=False)
    leaving_date = db.Column(db.String(20), nullable=False)
    reason_for_leaving = db.Column(db.String(200), nullable=True)