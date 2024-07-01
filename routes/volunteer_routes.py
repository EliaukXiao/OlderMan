from flask import Blueprint, request, jsonify
from models import db, VolunteerInfo

volunteer_bp = Blueprint('volunteer', __name__)

@volunteer_bp.route('/', methods=['GET'])
def get_volunteers():
    volunteers = VolunteerInfo.query.all()
    return jsonify([volunteer.to_dict() for volunteer in volunteers])

@volunteer_bp.route('/', methods=['POST'])
def add_volunteer():
    data = request.get_json()
    new_volunteer = VolunteerInfo(**data)
    db.session.add(new_volunteer)
    db.session.commit()
    return jsonify(new_volunteer.to_dict()), 201

# 添加其他CRUD操作，例如更新和删除志愿者信息
