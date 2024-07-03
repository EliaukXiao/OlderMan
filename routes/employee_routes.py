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
    total_count = len(employees)
    male_count = sum(1 for employee in employees if employee.gender == '1')
    female_count = sum(1 for employee in employees if employee.gender == '0')

    response = {
        "code": 0,
        "message": "Success",
        "data": [add_image_url(employee.to_dict()) for employee in employees],
        "total_count": total_count,
        "male_count": male_count,
        "female_count": female_count
    }
    return jsonify(response), 200
@employee_bp.route('/add', methods=['POST'])
def add_employee():
    data = request.get_json()
    required_fields = ['username', 'gender', 'phone', 'hire_date']


    # 检查用户名是否重复，重复则不允许新建
    if EmployeeInfo.query.filter_by(username=data['username']).first():
        return jsonify({"code": 1, "message": "Username already exists"}), 400

    # 检查是否缺少必填字段
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"code": 1, "message": f"Missing required field: {field}"}), 400

    # 创建新的 EmployeeInfo 实例
    new_employee = EmployeeInfo(
        username=data['username'],
        gender=data['gender'],
        phone=data['phone'],
        hire_date=data['hire_date'],
        imgset_dir='',
        description=data.get('description', ''),
        isCollected= False  # 默认为 False

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


#修改员工信息
@employee_bp.route('/update', methods=['PUT'])
def update_employee():
    data = request.get_json()
    user_id = data.get('id')

    if not user_id:
        return jsonify({"code": 1, "message": "Missing required field: id"}), 400

    employee = EmployeeInfo.query.get(user_id)
    if not employee:
        return jsonify({"code": 1, "message": "Employee not found"}), 404

    required_fields = ['gender', 'phone', 'hire_date','description']

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"code": 1, "message": f"Missing required field: {field}"}), 400

    employee.gender = data['gender']
    employee.phone = data['phone']
    employee.hire_date = data['hire_date']
    employee.description = data.get('description', '')

    db.session.commit()

    response = {
        "code": 0,
        "message": "Employee updated successfully",
        "data": add_image_url(employee.to_dict())
    }

    return jsonify(response), 200

#删除老年人信息
@employee_bp.route('/delete', methods=['DELETE'])
def delete_employee():
    data=request.get_json()
    user_id=data.get('id')
    if not user_id:
        return jsonify({"code": 1, "message": "Missing required field: id"}), 400

    employee = EmployeeInfo.query.get(user_id)

    if not employee:
        return jsonify({"code": 1, "message": "Employee not found"}), 404
    db.session.delete(employee)
    db.session.commit()

    response = {
        "code": 0,
        "message": "Employee deleted successfully",
        "data": add_image_url(employee.to_dict())
    }

    return jsonify(response), 200
