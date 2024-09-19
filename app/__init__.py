from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_download_btn import DownloadBtnManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
download_btn_manager = DownloadBtnManager(app, db=db)

from app import routes, models