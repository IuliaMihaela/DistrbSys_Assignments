from flask import Flask, request
from flask_restful import Resource, Api
import uuid

app = Flask(__name__)
api = Api(app)


# Authentication Service

users = {}

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
    return users[data["username"]]["role"]+'-'+str(uuid.uuid1())

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



# Master Data Service

# jobs ={id:{
#         user:""
#         timestamp:""
#         status:""
#         date_range:""
#         assets:""}
#        }

jobs = {}

def validate_post_job(data):
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "no token provided"}
    if "timestamp" not in data:
        return {"error": "no timestamp provided"}
    if "status" not in data:
        return {"error": "status not provided"}
    if "date_range" not in data:
        return {"error": "date_range not provided"}
    if "assets" not in data:
        return {"error": "assets not provided"}
    return ""

def validate_get_job(data):
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "no token provided"}
    if "job_id" not in data:
        return {"error": "no job_id provided"}
    return ""

def validate_update_job(data):
    if "job_id" not in data:
        return {"error": "no job_id provided"}
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "no token provided"}
    if "timestamp" not in data:
        return {"error": "no timestamp provided"}
    if "status" not in data:
        return {"error": "status not provided"}
    if "date_range" not in data:
        return {"error": "date_range not provided"}
    if "assets" not in data:
        return {"error": "assets not provided"}
    return ""

def validate_user_permission_master_data(username, token):
    token_state = verify_token(username, token)
    if token_state['success'] == True:
        return {"error": "Token not valid"}
    if username not in users.keys() or token.split('-')[0] == "secretary":
        return {"error": "Authorization Error"}
    return ""


def create_job(data):
    new_job_id = str(uuid.uuid1())
    del data["token"]
    new_job = {new_job_id:data}
    jobs.update(new_job)
    return new_job

# def submit_job(job):
#     jobs.update(job)
#     return job

def fetch_job(job_id):
    return jobs[job_id]

def update_job(data):
    job_data = jobs[data["id"]]
    id=data['id']
    del data["id"]
    jobs[id] = job_data
    return jobs[id]

class Jobs(Resource):
    def post(self):
        validation = validate_post_job(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"], data["token"])
        if validation != "":
            return validation

        new_job = create_job(request.json)
        return new_job

    def get(self):
        validation = validate_get_job(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"],data["token"])
        if validation != "":
            return validation
        job = fetch_job(data["id"])
        return job

    def put(self):
        validation = validate_update_job(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"], data["token"])
        if validation != "":
            return validation
        updated_job = update_job(request.json)
        return updated_job

class Results(Resource):
    pass


api.add_resource(Jobs, '/jobs/api')
api.add_resource(Results, '/results/api')


##### NOTES ####
# only token as in-memory cash, the rest of user data as persistent storage ?
# persistent storage: pickle, json, sql lite ?
# tokens expire ?
# separate resources ?



if __name__ == '__main__':
    app.run(debug=True)


