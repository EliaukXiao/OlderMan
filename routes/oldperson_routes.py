from flask import Blueprint, request, jsonify
from models import db, OldPersonInfo

oldperson_bp = Blueprint('oldperson', __name__)

@oldperson_bp.route('/', methods=['GET'])
def get_oldpersons():
    oldpersons = OldPersonInfo.query.all()
    return jsonify([oldperson.to_dict() for oldperson in oldpersons])

@oldperson_bp.route('/', methods=['POST'])
def add_oldperson():
    data = request.get_json()
    new_oldperson = OldPersonInfo(**data)
    db.session.add(new_oldperson)
    db.session.commit()
    return jsonify(new_oldperson.to_dict()), 201

# 添加其他CRUD操作
