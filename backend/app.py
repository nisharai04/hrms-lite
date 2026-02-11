import os
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.models import db, Employee, Attendance


# ---------------------------------
# PATH SETUP
# ---------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# ---------------------------------
# CREATE FLASK APP
# ---------------------------------
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

# ---------------------------------
# DATABASE CONFIG
# ---------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hrms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()

# ---------------------------------
# FRONTEND ROUTES
# ---------------------------------

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# ---------------------------------
# HELPER
# ---------------------------------

def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

# =================================
# EMPLOYEE APIs
# =================================

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json

    if not data or not all(k in data for k in ("employee_id", "full_name", "email", "department")):
        return jsonify({"error": "All fields are required"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    if Employee.query.filter_by(employee_id=data["employee_id"]).first():
        return jsonify({"error": "Employee ID already exists"}), 400

    emp = Employee(
        employee_id=data["employee_id"],
        full_name=data["full_name"],
        email=data["email"],
        department=data["department"]
    )

    db.session.add(emp)
    db.session.commit()

    return jsonify({"message": "Employee added successfully"}), 201


@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    return jsonify([
        {
            "id": e.id,
            "employee_id": e.employee_id,
            "full_name": e.full_name,
            "email": e.email,
            "department": e.department
        }
        for e in employees
    ]), 200


@app.route("/employees/<int:id>", methods=["DELETE"])
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

@app.route("/attendance", methods=["POST"])
def mark_attendance():
    data = request.json

    if not data or not all(k in data for k in ("employee_id", "date", "status")):
        return jsonify({"error": "All fields are required"}), 400

    employee = Employee.query.get(data["employee_id"])
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    record = Attendance(
        employee_id=data["employee_id"],
        date=data["date"],
        status=data["status"]
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Attendance marked"}), 201


@app.route("/attendance/<int:employee_id>", methods=["GET"])
def get_attendance(employee_id):
    records = Attendance.query.filter_by(employee_id=employee_id).all()
    return jsonify([
        {"date": r.date, "status": r.status}
        for r in records
    ]), 200

# ---------------------------------
# RUN SERVER
# ---------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
