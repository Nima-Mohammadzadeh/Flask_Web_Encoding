from flask_socketio import SocketIO
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
socketio = SocketIO(app , cors_allowed_origins="*")
migrate = Migrate(app, db)

from app import routes, models