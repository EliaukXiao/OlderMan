from app import app
from models import db, AdminUser

with app.app_context():
    db.create_all()

    admin1 = AdminUser(username='CF', real_name='曹帆', gender='Female', email='admin1@example.com', phone='1234567890', description='Super Admin')
    admin1.set_password('cf123456')

    admin2 = AdminUser(username='LX', real_name='刘逍', gender='Female', email='admin2@example.com', phone='2345678901', description='Admin User')
    admin2.set_password('lx123456')

    admin3 = AdminUser(username='DYH', real_name='丁宇涵', gender='Female', email='admin3@example.com', phone='3456789012', description='Regular Admin')
    admin3.set_password('dyh123456')

    db.session.add(admin1)
    db.session.add(admin2)
    db.session.add(admin3)
    db.session.commit()
