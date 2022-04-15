from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)  # create Flask application
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master_data.db'

# db provides a class called Model that is a declarative base which can be used to declare models
db = SQLAlchemy(app)

from services import authentication_service, master_data_service

