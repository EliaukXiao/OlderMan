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

# 其他CRUD操作
