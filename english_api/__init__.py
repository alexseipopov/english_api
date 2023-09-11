import logging
import os

from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["UPLOAD_FOLDER"] = '/app/english_api/static/materials'
app.config["UPLOAD_FOLDER_AUDIO"] = '/app/english_api/static/materials'  # os.environ["UPLOAD_FOLDER"]
app.config["UPLOAD_FOLDER_IMAGE"] = '/app/english_api/static/materials'  # os.environ["UPLOAD_FOLDER"]
logging.basicConfig(level=logging.DEBUG, format=' - [%(asctime)s] [%(process)d] [%(levelname)s] %(message)s')

swagger = Swagger(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from .admin import admin as ad
from .api import api as api_

app.register_blueprint(api_)

with app.app_context():
    db.create_all()
