from flask import Blueprint, request, jsonify
from models import db, OldPersonInfo

oldperson_bp = Blueprint('oldperson', __name__)

def add_image_url(data):
    if not data['imgset_dir']:
        data['imgset_dir'] = request.host_url + 'static/orderMan.jpg'
    else:
        data['imgset_dir'] = request.host_url + data['imgset_dir']
    return data

@oldperson_bp.route('/', methods=['GET'])
def get_oldpersons():
    oldpersons = OldPersonInfo.query.all()
    response = {
        "code": 0,
        "message": "Success",
        "data": [add_image_url(oldperson.to_dict()) for oldperson in oldpersons]
    }
    return jsonify(response), 200

@oldperson_bp.route('/', methods=['POST'])
def add_oldperson():
    data = request.get_json()
    required_fields = ['username', 'gender', 'phone', 'id_card', 'birthday', 'checkin_date', 'room_number', 'health_state']

    # Check for missing required fields
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"code": 1, "message": f"Missing required field: {field}"}), 400

    # Create new OldPersonInfo instance
    new_oldperson = OldPersonInfo(
        username=data['username'],
        gender=data['gender'],
        phone=data['phone'],
        id_card=data['id_card'],
        birthday=data['birthday'],
        checkin_date=data['checkin_date'],
        room_number=data['room_number'],
        health_state=data['health_state'],
        checkout_date=data.get('checkout_date'),
        imgset_dir=data.get('imgset_dir', 'static/orderMan.jpg'),  # Set default image path if not provided
        firstguardian_name=data.get('firstguardian_name', ''),
        firstguardian_relationship=data.get('firstguardian_relationship', ''),
        firstguardian_phone=data.get('firstguardian_phone', ''),
        firstguardian_wechat=data.get('firstguardian_wechat', ''),
        secondguardian_name=data.get('secondguardian_name', ''),
        secondguardian_relationship=data.get('secondguardian_relationship', ''),
        secondguardian_phone=data.get('secondguardian_phone', ''),
        secondguardian_wechat=data.get('secondguardian_wechat', '')
    )

    db.session.add(new_oldperson)
    db.session.commit()

    response = {
        "code": 0,
        "message": "Old person added successfully",
        "data": add_image_url(new_oldperson.to_dict())
    }
    return jsonify(response), 201


@oldperson_bp.route('/search', methods=['GET'])
def search_oldpersons():
    query = OldPersonInfo.query
    filters = {}

    if 'id' in request.args:
        filters['id'] = request.args.get('id')
    if 'username' in request.args:
        filters['username'] = request.args.get('username')
    if 'gender' in request.args:
        filters['gender'] = request.args.get('gender')
    if 'room_number' in request.args:
        filters['room_number'] = request.args.get('room_number')
    if 'health_state' in request.args:
        filters['health_state'] = request.args.get('health_state')

    for attr, value in filters.items():
        if value:
            query = query.filter(getattr(OldPersonInfo, attr).like(f"%{value}%"))

    oldpersons = query.all()
    response = {
        "code": 0,
        "message": "Success",
        "data": [add_image_url(oldperson.to_dict()) for oldperson in oldpersons]
    }
    return jsonify(response), 200

# 其他CRUD操作