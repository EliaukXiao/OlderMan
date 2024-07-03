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
    total_count = len(oldpersons)
    male_count = sum(1 for person in oldpersons if person.gender == '1')
    female_count = sum(1 for person in oldpersons if person.gender == '0')

    response = {
        "code": 0,
        "message": "Success",
        "data": [add_image_url(oldperson.to_dict()) for oldperson in oldpersons],
        "total_count": total_count,
        "male_count": male_count,
        "female_count": female_count
    }
    return jsonify(response), 200


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


@oldperson_bp.route('/update', methods=['PUT'])
def update_oldperson():
    data = request.get_json()
    user_id = data.get('id')

    if not user_id:
        return jsonify({"code": 1, "message": "Missing required field: id"}), 400

    old_person = OldPersonInfo.query.get(user_id)
    if not old_person:
        return jsonify({"code": 1, "message": "Old person not found"}), 404

    required_fields = ['gender', 'phone', 'id_card', 'birthday', 'checkin_date', 'room_number', 'health_state']

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"code": 1, "message": f"Missing required field: {field}"}), 400

    old_person.gender = data['gender']
    old_person.phone = data['phone']
    old_person.id_card = data['id_card']
    old_person.birthday = data['birthday']
    old_person.checkin_date = data['checkin_date']
    old_person.room_number = data['room_number']
    old_person.firstguardian_name = data.get('firstguardian_name', '')
    old_person.firstguardian_relationship = data.get('firstguardian_relationship', '')
    old_person.firstguardian_phone = data.get('firstguardian_phone', '')
    old_person.firstguardian_wechat = data.get('firstguardian_wechat', '')
    old_person.secondguardian_name = data.get('secondguardian_name', '')
    old_person.secondguardian_relationship = data.get('secondguardian_relationship', '')
    old_person.secondguardian_phone = data.get('secondguardian_phone', '')
    old_person.secondguardian_wechat = data.get('secondguardian_wechat', '')
    old_person.health_state = data['health_state']

    db.session.commit()

    response = {
        "code": 0,
        "message": "Old person information updated successfully",
        "data": add_image_url(old_person.to_dict())
    }
    return jsonify(response), 200

# 其他CRUD操作

@oldperson_bp.route('/delete', methods=['DELETE'])
def delete_oldperson():
    data = request.get_json()
    user_id = data.get('id')

    if not user_id:
        return jsonify({"code": 1, "message": "Missing required field: id"}), 400

    old_person = OldPersonInfo.query.get(user_id)
    if not old_person:
        return jsonify({"code": 1, "message": "Old person not found"}), 404

    db.session.delete(old_person)
    db.session.commit()

    response = {
        "code": 0,
        "message": "Old person deleted successfully"
    }
    return jsonify(response), 200


@oldperson_bp.route('/add', methods=['POST'])
def add_oldperson():
    data = request.get_json()
    required_fields = [
        'username', 'gender', 'phone', 'id_card', 'birthday',
        'checkin_date', 'room_number', 'health_state',
        'firstguardian_name', 'firstguardian_relationship', 'firstguardian_phone',
        # 'firstguardian_wechat', 'secondguardian_name', 'secondguardian_relationship',
        # 'secondguardian_phone', 'secondguardian_wechat'
    ]

    # 检查用户名是否重复，重复则不允许新建
    # Check if username already exists
    existing_oldperson = OldPersonInfo.query.filter_by(username=data['username']).first()
    if existing_oldperson:
        return jsonify({"code": 1, "message": "Username already exists"}), 400

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
        firstguardian_name=data['firstguardian_name'],
        firstguardian_relationship=data['firstguardian_relationship'],
        firstguardian_phone=data['firstguardian_phone'],
        firstguardian_wechat=data.get('firstguardian_wechat', ''),
        secondguardian_name=data.get('secondguardian_name', ''),
        secondguardian_relationship=data.get('secondguardian_relationship', ''),
        secondguardian_phone=data.get('secondguardian_phone', ''),
        secondguardian_wechat=data.get('secondguardian_wechat', ''),
        imgset_dir='',
        isCollected=False
    )

    db.session.add(new_oldperson)
    db.session.commit()

    response = {
        "code": 0,
        "message": "Old person added successfully",
        "data": add_image_url(new_oldperson.to_dict())
    }
    return jsonify(response), 201
