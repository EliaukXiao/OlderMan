from flask import Blueprint, request, jsonify
from models import db, EmployeeInfo

employee_bp = Blueprint('employee', __name__)

def add_image_url(data):
    if not data['imgset_dir']:
        data['imgset_dir'] = request.host_url + 'static/employee.jpg'
    else:
        data['imgset_dir'] = request.host_url + data['imgset_dir']
    return data

@employee_bp.route('/all', methods=['GET'])
def get_employees():
    employees = EmployeeInfo.query.all()
    response = {
        "code": 0,
        "message": "Success",
        "data": [add_image_url(employee.to_dict()) for employee in employees]
    }
    return jsonify(response), 200

@employee_bp.route('/', methods=['POST'])
def add_employee():
    data = request.get_json()
    required_fields = ['username', 'gender', 'phone', 'birthday', 'hire_date']

    # 检查是否缺少必填字段
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"code": 1, "message": f"Missing required field: {field}"}), 400

    # 创建新的 EmployeeInfo 实例
    new_employee = EmployeeInfo(
        username=data['username'],
        gender=data['gender'],
        phone=data['phone'],
        birthday=data['birthday'],
        hire_date=data['hire_date'],
        resign_date=data.get('resign_date'),
        imgset_dir=data.get('imgset_dir', 'static/employee.jpg'),  # 设置默认图像路径
        description=data.get('description', '')
    )

    try:
        db.session.add(new_employee)
        db.session.commit()
        response = {
            "code": 0,
            "message": "Employee added successfully",
            "data": add_image_url(new_employee.to_dict())
        }
        return jsonify(response), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 2, "message": "An error occurred while adding the employee", "error": str(e)}), 500


@employee_bp.route('/search', methods=['GET'])
def search_employees():
    query = EmployeeInfo.query
    filters = {}

    if 'id' in request.args:
        filters['id'] = request.args.get('id')
    if 'username' in request.args:
        filters['username'] = request.args.get('username')
    if 'gender' in request.args:
        filters['gender'] = request.args.get('gender')

    for attr, value in filters.items():
        if value:
            query = query.filter(getattr(EmployeeInfo, attr).like(f"%{value}%"))

    employees = query.all()
    response = {
        "code": 0,
        "message": "Success",
        "data": [add_image_url(employee.to_dict()) for employee in employees]
    }
    return jsonify(response), 200
# 添加其他CRUD操作，例如更新和删除员工信息
