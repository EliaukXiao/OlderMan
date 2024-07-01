from app import app
from models import db, OldPersonInfo
from datetime import datetime

with app.app_context():
    db.create_all()

    old_person1 = OldPersonInfo(
        username='John Doe',
        gender='1',
        phone='1234567890',
        id_card='123456789012345678',
        birthday=datetime(1940, 1, 1),
        checkin_date=datetime(2022, 1, 1),
        room_number='101',
        firstguardian_name='Jane Doe',
        firstguardian_relationship='Daughter',
        firstguardian_phone='0987654321',
        firstguardian_wechat='jane_doe',
        secondguardian_name='Joe Doe',
        secondguardian_relationship='Son',
        secondguardian_phone='0987654322',
        secondguardian_wechat='joe_doe',
        health_state='Good'
    )

    old_person2 = OldPersonInfo(
        username='Alice Smith',
        gender='0',
        phone='2345678901',
        id_card='234567890123456789',
        birthday=datetime(1935, 5, 15),
        checkin_date=datetime(2021, 6, 1),
        room_number='102',
        firstguardian_name='Bob Smith',
        firstguardian_relationship='Son',
        firstguardian_phone='1987654321',
        firstguardian_wechat='bob_smith',
        secondguardian_name='Cathy Smith',
        secondguardian_relationship='Daughter',
        secondguardian_phone='2987654322',
        secondguardian_wechat='cathy_smith',
        health_state='Fair'
    )

    db.session.add(old_person1)
    db.session.add(old_person2)
    db.session.commit()
