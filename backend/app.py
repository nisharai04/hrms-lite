import os
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Employee, Attendance

# ---------------------------------
# PATH SETUP FOR FRONTEND FOLDER
# ---------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

# Create Flask app
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()

# ---------------------------------
# SERVE FRONTEND FILES
# ---------------------------------

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/employees-page")
def serve_employees_page():
    return send_from_directory(FRONTEND_DIR, "employees.html")

@app.route("/attendance-page")
def serve_attendance_page():
    return send_from_directory(FRONTEND_DIR, "attendance.html")

# Serve CSS & JS files
@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# ---------------------------------
# HELPER FUNCTION
# ---------------------------------

def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

# =================================
# EMPLOYEE APIs
# =================================

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json

    if not data or not all(k in data for k in ("employee_id", "full_name", "email", "department")):
        return jsonify({"error": "All fields are required"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    if Employee.query.filter_by(employee_id=data["employee_id"]).first():
        return jsonify({"error": "Employee ID already exists"}), 400

    new_employee = Employee(
        employee_id=data["employee_id"],
        full_name=data["full_name"],
        email=data["email"],
        department=data["department"]
    )

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Employee added successfully"}), 201


@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()

    result = []
    for emp in employees:
        result.append({
            "id": emp.id,
            "employee_id": emp.employee_id,
            "full_name": emp.full_name,
            "email": emp.email,
            "department": emp.department
        })

    return jsonify(result), 200


@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    emp = Employee.query.get(id)

    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(emp)
    db.session.commit()

    return jsonify({"message": "Employee deleted"}), 200


# =================================
# ATTENDANCE APIs
# =================================

@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.json

    if not data or not all(k in data for k in ("employee_id", "date", "status")):
        return jsonify({"error": "All fields are required"}), 400

    employee = Employee.query.get(data["employee_id"])
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    attendance = Attendance(
        employee_id=data["employee_id"],
        date=data["date"],
        status=data["status"]
    )

    db.session.add(attendance)
    db.session.commit()

    return jsonify({"message": "Attendance marked"}), 201


@app.route('/attendance/<int:employee_id>', methods=['GET'])
def get_attendance(employee_id):
    records = Attendance.query.filter_by(employee_id=employee_id).all()

    result = []
    for record in records:
        result.append({
            "date": record.date,
            "status": record.status
        })

    return jsonify(result), 200


# =================================
# RUN SERVER
# =================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
