from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

users={}

class User(Resource):
    pass







if __name__ == '__main__':
    app.run(debug=True)
