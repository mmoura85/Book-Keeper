from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
# from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)

# Initialize config file
app.config.from_object('config')

# Initialize plugins

# # orm plugin
db = SQLAlchemy(app)

# import stuff

from app import views, models

__all__ = ['views', 'models', ]
