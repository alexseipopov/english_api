import logging
import os
from logging.handlers import MemoryHandler

from flasgger import Swagger, swag_from
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["UPLOAD_FOLDER"] = '/app/english_api/static/materials'
app.config["UPLOAD_FOLDER_AUDIO"] = '/app/english_api/static/materials'  # os.environ["UPLOAD_FOLDER"]
app.config["UPLOAD_FOLDER_IMAGE"] = '/app/english_api/static/materials'  # os.environ["UPLOAD_FOLDER"]

# logging.basicConfig(level=logging.DEBUG, format=' - [%(asctime)s] [%(process)d] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s')
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)

memory_handler = MemoryHandler(capacity=100, flushLevel=logging.ERROR, target=stream_handler)
memory_handler.setLevel(logging.DEBUG)
logger.addHandler(memory_handler)

swagger = Swagger(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.get("/logs")
@swag_from({
    "tags": ["Logs"],
    "description": "Returns logs",
    "responses": {
        "200": {
            "description": "Logs"
        }
    }
})
def logs():
    records = [record for record in memory_handler.buffer]
    log_entries = [stream_formatter.format(record) for record in records]
    log_entries = [log_entry.replace('\r', ' ') for log_entry in log_entries]
    log_entries = [log_entry.replace('\n', ' ') for log_entry in log_entries]
    return jsonify(log_entries)


from .admin import admin as ad
from .api import api as api_

app.register_blueprint(api_)

with app.app_context():
    db.create_all()
