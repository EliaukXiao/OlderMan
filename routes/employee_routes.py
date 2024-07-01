from flask import Blueprint, request, jsonify
from models import db, EmployeeInfo

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/', methods=['GET'])
def get_employees():
    employees = EmployeeInfo.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@employee_bp.route('/', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_employee = EmployeeInfo(**data)
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(new_employee.to_dict()), 201

# 添加其他CRUD操作，例如更新和删除员工信息
