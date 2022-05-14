from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)  # create Flask application
api = Api(app)


app2 = Flask(__name__)  # create Flask application message queues
api2 = Api(app2)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master_data.db'

# app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///message_queues.db'

# db provides a class called Model that is a declarative base which can be used to declare models
db = SQLAlchemy(app)

db2 = SQLAlchemy(app2)

from services import authentication_service, master_data_service, message_queues_service

