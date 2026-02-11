from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    attendance = db.relationship('Attendance', backref='employee', cascade="all, delete")

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # Present / Absent
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
