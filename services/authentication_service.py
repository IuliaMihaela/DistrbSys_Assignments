from flask import request  #,Flask
from flask_restful import Resource #, Api
import uuid
from services import api

# Authentication Service

users = {}

def validate_registration(data):
    # check if the password and the role were provided by the client
    if "password" not in data:
        return {"error": "no password provided"}
    if "role" not in data:
        return {"error": "no role provided"}
    return ""

def validate_login(data):
    # check if the username and the password were provided
    if "username" not in data:
        return {"error": "no username provided"}
    if "password" not in data:
        return {"error": "no password provided"}
    # check if the password provided is correct
    if data["password"] != users[data["username"]]["password"]:
        return {"error": "password not correct"}
    return ""

def emit_token(data):
    # creating the token containing the user role and a random string
    return users[data["username"]]["role"]+'-'+str(uuid.uuid1())

class Registration(Resource):
    def post(self, username):
        validation = validate_registration(request.json)
        if validation != "":
            return validation
        new_username = username
        # if the username is already taken, we add a number next to it
        if username in users:
            n = 1
            while new_username in users:
                new_username = f'{username}{n}'
                n = n + 1
        users[new_username] = request.json
        return {new_username: users[new_username]}

class Login(Resource):
    def put(self):
        validation = validate_login(request.json)
        if validation != "":
            return validation
        data = request.json
        # the user gets a token if logged in
        token = emit_token(data)
        users[data["username"]].update({"token": token})
        return {data["username"]: users[data["username"]]}

def verify_token(username,token):
    # checking if the token given corresponds with the one stored
    if users[username]["token"] != token:
        return {"success": False}
    return {"success": True}


api.add_resource(Registration, '/users/registration/api/<string:username>')
api.add_resource(Login, '/users/login/api')
