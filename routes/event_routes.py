from flask import Blueprint, request, jsonify
from models import db, EventInfo

event_bp = Blueprint('event', __name__)

@event_bp.route('/', methods=['GET'])
def get_events():
    events = EventInfo.query.all()
    return jsonify([event.to_dict() for event in events])

@event_bp.route('/', methods=['POST'])
def add_event():
    data = request.get_json()
    new_event = EventInfo(**data)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201

# 添加其他CRUD操作，例如更新和删除事件信息
