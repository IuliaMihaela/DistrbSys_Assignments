from flask import request, jsonify #,Flask
from flask_restful import Resource #, Api
import uuid
# from flask_sqlalchemy import SQLAlchemy
from services import app, api, db
from services.models import Job, Result

# app = Flask(__name__)
# api = Api(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master_data.db'
# db = SQLAlchemy(app)



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
    return {"success": True}


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

def create_response(message):
    return {
        "source": "http://127.0.0.1:5000",
        "destination": "",
        "message_body": message
    }
    # return jsonify(
    #     source="http://127.0.0.1:5000",
    #     destination="",
    #     message_body=message
    # )

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

def validate_get_delete_job_result(data):
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
    if token_state['success'] == False:
        return {"error": "Token not valid"}
    if username not in users.keys() or token.split('-')[0] == "secretary":
        return {"error": "Authorization Error"}
    return ""


def create_job(data):
    # new_job_id = str(uuid.uuid1())
    # del data["token"]
    # new_job = {new_job_id:data}
    # jobs.update(new_job)
    # return new_job

    ### sql ###
    new_job_id = str(uuid.uuid1())
    new_job = Job(id=new_job_id, username=data['username'], timestamp=data['timestamp'], status=data['status'], date_range=data['date_range'], assets=data['assets'])
    db.session.add(new_job)  # add job to database
    db.session.commit()  # save changes to database
    return new_job.serialize()


def fetch_job(job_id):
    # return {job_id: jobs[job_id]}

    ### sql ###
    try:
        job = Job.query.get(job_id)
        return job.serialize()
    except:
        return "Job not found"

def update_job(data):
    # job_data = jobs[data["job_id"]]
    # id=data['job_id']
    # del data["job_id"]
    # del data["token"]
    # jobs[id] = data
    # return{id: jobs[id]}

    ### sql ###
    id = data['job_id']
    job = Job.query.get(id)
    job.username = data['username']
    job.timestamp = data['timestamp']
    job.status = data['status']
    job.date_range = data['date_range']
    job.assets = data['assets']
    db.session.commit()
    return job.serialize()

def delete_job(job_id):
    try:
        job = Job.query.get(job_id)
        db.session.delete(job)
        db.session.commit()
        return {"success": True}
    except:
        return "Job not found"

class Jobs(Resource):
    def post(self):
        validation = validate_post_job(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"], data["token"])  # check if the user has permission
        if validation != "":
            return validation

        new_job = create_job(request.json)
        response = create_response(new_job)
        return response

    def get(self):
        validation = validate_get_delete_job_result(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"],data["token"])
        if validation != "":
            return validation
        job = fetch_job(data["job_id"])
        response = create_response(job)
        return response

    def put(self):
        validation = validate_update_job(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"], data["token"])
        if validation != "":
            return validation
        updated_job = update_job(request.json)
        response = create_response(updated_job)
        return response

    def delete(self):
        validation = validate_get_delete_job_result(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"], data["token"])
        if validation != "":
            return validation
        deleted_job_response = delete_job(data["job_id"])
        response = create_response(deleted_job_response)
        return response

########## Results ###########

def validate_post_result(data):
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "no token provided"}
    if "job_id" not in data:
        return {"error": "job_id not provided"}
    if "timestamp" not in data:
        return {"error": "no timestamp provided"}
    if "assets" not in data:
        return {"error": "assets not provided"}
    return ""

# def validate_get_delete_result(data):
#     if "username" not in data:
#         return {"error": "no user provided"}
#     if "token" not in data:
#         return {"error": "no token provided"}
#     if "job_id" not in data:
#         return {"error": "no job_id provided"}
#     return ""
#
# def validate_update_result(data):
#     if "job_id" not in data:
#         return {"error": "no job_id provided"}
#     if "username" not in data:
#         return {"error": "no user provided"}
#     if "token" not in data:
#         return {"error": "no token provided"}
#     if "timestamp" not in data:
#         return {"error": "no timestamp provided"}
#     if "status" not in data:
#         return {"error": "status not provided"}
#     if "date_range" not in data:
#         return {"error": "date_range not provided"}
#     if "assets" not in data:
#         return {"error": "assets not provided"}
#     return ""

def validate_update_result(data):
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "no token provided"}
    if "job_id" not in data:
        return {"error": "job_id not provided"}
    if "new_job_id" not in data:
        return {"error": "new_job_id not provided"}
    if "timestamp" not in data:
        return {"error": "no timestamp provided"}
    if "assets" not in data:
        return {"error": "assets not provided"}
    return ""


def create_result(data):
    new_result = Result(job_id=data['job_id'], timestamp=data['timestamp'], assets=data['assets'])
    db.session.add(new_result)  # add job to database
    db.session.commit()  # save changes to database
    return new_result.serialize()

def fetch_result(job_id):
    try:
        result = Result.query.get(job_id)
        return result.serialize()
    except:
        return "Result not found"

def update_result(data):
    id = data['job_id']
    result = Result.query.get(id)
    result.job_id = data['username']
    result.timestamp = data['timestamp']
    result.assets = data['assets']
    db.session.commit()
    return result.serialize()


class Results(Resource):
    pass

api.add_resource(Jobs, '/jobs/api')
api.add_resource(Results, '/results/api')


##### NOTES ####
# only token as in-memory cash, the rest of user data as persistent storage ?
# persistent storage: pickle, json, sql lite ?
# tokens expire ?
# separate services ?
# Registration needed ?
# Request, responses with source,....
# timestamp datetime module
# When to call results table
# for master data service you need only the token or also the username (checking for permissions) ?
# readme.md file !!!!

if __name__ == '__main__':
    app.run(debug=True)


