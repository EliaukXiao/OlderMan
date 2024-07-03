from flask import Blueprint, request, jsonify
from models import db, AdminUser

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = AdminUser.query.filter_by(username=username).first()
    if user and user.check_password(password):
        response = {
            "message": "Login successful",
            "code": 0,
            "user": user.to_dict()
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "Invalid username or password",
            "code": 1
        }
        return jsonify(response), 401

@admin_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    real_name = data.get('real_name')
    gender = data.get('gender')
    email = data.get('email')
    phone = data.get('phone')
    description = data.get('description', '')

    if gender not in ['0', '1']:
        return jsonify({"message": "Invalid gender value", "code": 2}), 400

    if AdminUser.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists", "code": 1}), 400

    new_user = AdminUser(
        username=username,
        real_name=real_name,
        gender=gender,
        email=email,
        phone=phone,
        description=description
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful", "code": 0, "user": new_user.to_dict()}), 201
@admin_bp.route('/all', methods=['GET'])
def get_all_admins():
    admins = AdminUser.query.all()
    response = {
        "code": 0,
        "message": "Success",
        "data": [admin.to_dict() for admin in admins]
    }
    return jsonify(response), 200


@admin_bp.route('/<username>', methods=['GET'])
def get_admin_by_username(username):
    user = AdminUser.query.filter_by(username=username).first()
    if user:
        response = {
            "code": 0,
            "message": "Success",
            "data": user.to_dict()
        }
        return jsonify(response), 200
    else:
        response = {
            "code": 1,
            "message": "User not found"
        }
        return jsonify(response), 404
# 其他CRUD操作
@admin_bp.route('/update_password', methods=['PUT'])
def update_password():
    data = request.get_json()
    user_id = data.get('id')
    new_password = data.get('new_password')

    if not user_id or not new_password:
        return jsonify({"message": "Missing required fields", "code": 1}), 400

    user = AdminUser.query.get(user_id)
    if user:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "Password updated successfully", "code": 0}), 200
    else:
        return jsonify({"message": "User not found", "code": 1}), 404



@admin_bp.route('/update_info', methods=['PUT'])
def update_info():
    data = request.get_json()
    user_id = data.get('id')
    username = data.get('username')
    real_name = data.get('real_name')
    gender = data.get('gender')
    email = data.get('email')
    phone = data.get('phone')
    description = data.get('description')

    if not user_id or not username or not real_name or not gender or not email or not phone:
        return jsonify({"message": "Missing required fields", "code": 1}), 400

    if AdminUser.query.filter(AdminUser.username == username, AdminUser.id != user_id).first():
        return jsonify({"message": "Username already exists", "code": 1}), 400

    user = AdminUser.query.get(user_id)
    if user:
        user.username = username
        user.real_name = real_name
        user.gender = gender
        user.email = email
        user.phone = phone
        user.description = description
        db.session.commit()
        return jsonify({"message": "Information updated successfully", "code": 0}), 200
    else:
        return jsonify({"message": "User not found", "code": 1}), 404

# 其他CRUD操作