from flask import Flask, request
from flask_restful import Resource, Api
import uuid

app = Flask(__name__)
api = Api(app)

users = {}

def authentication(username, password):
    pass

def validate_registration(data):
    # if "username" not in data:
    #     return {"error": "no username provided"}
    if "password" not in data:
        return {"error": "no password provided"}
    if "role" not in data:
        return {"error": "no role provided"}
    return ""

def validate_login(data):
    if "username" not in data:
        return {"error": "no username provided"}
    if "password" not in data:
        return {"error": "no password provided"}
    if data["password"] != users[data["username"]]["password"]:
        return {"error": "password not correct"}
    return ""

def emit_token(data):
    return users[data["username"]]["role"]+str(uuid.uuid1())

class Registration(Resource):
    def post(self, username):
        validation = validate_registration(request.json)
        if validation != "":
            return validation
        # data=request.json
        # username=data["username"]
        new_username = username
        if username in users:
            n = 1
            while new_username in users:
                bird_new_name = f'{username}{n}'
                n = n + 1
        users[new_username] = request.json
        return {new_username: users[new_username]}

class Login(Resource):
    def put(self):
        validation = validate_login(request.json)
        if validation != "":
            return validation
        data=request.json
        # return {data["username"]: users[data["username"]]}
        token = emit_token(data)
        users[data["username"]].update({"token": token})
        return {data["username"]: users[data["username"]]}

def verify_token(username,token):
    if users[username]["token"] != token:
        return {"success": False}
    return {"success": True }




api.add_resource(Registration, '/users/registration/api/<string:username>')
api.add_resource(Login, '/users/login/api')

class User(Resource):
    pass

#str(uuid.uuid1())





if __name__ == '__main__':
    app.run(debug=True)
