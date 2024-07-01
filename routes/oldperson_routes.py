from flask import Blueprint, request, jsonify
from models import db, OldPersonInfo

oldperson_bp = Blueprint('oldperson', __name__)

@oldperson_bp.route('/', methods=['GET'])
def get_oldpersons():
    oldpersons = OldPersonInfo.query.all()
    response = {
        "code": 0,
        "message": "Success",
        "data": [oldperson.to_dict() for oldperson in oldpersons]
    }
    return jsonify(response), 200

@oldperson_bp.route('/', methods=['POST'])
def add_oldperson():
    data = request.get_json()
    new_oldperson = OldPersonInfo(**data)
    db.session.add(new_oldperson)
    db.session.commit()
    response = {
        "code": 0,
        "message": "Old person added successfully",
        "data": new_oldperson.to_dict()
    }
    return jsonify(response), 201

# 其他CRUD操作

