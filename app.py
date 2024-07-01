from flask import Flask
from config import Config
from models import db, bcrypt
from routes import init_routes
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
bcrypt.init_app(app)
db.init_app(app)

# 配置 CORS
CORS(app)

with app.app_context():
    db.create_all()

init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
