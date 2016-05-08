from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import zlib
import redis
app = Flask(__name__)
app.config.from_object('config')

# SQLAlchamy is not used in current version, Redis server is used instead
db = SQLAlchemy(app)
r_server = redis.Redis()

from app import views, models
