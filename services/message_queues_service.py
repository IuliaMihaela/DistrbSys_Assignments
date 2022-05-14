import queue
from flask import request
from flask_restful import Resource
from master_data_service import *
from authentication_service import *
import uuid
from services import api2, db2

queue_jobs = queue.Queue
queue_results = queue.Queue

def validate_user_permission_append_pull(username, token):
    token_state = verify_token(username, token)
    # checking if the token is valid
    if token_state['success'] == False:
        return {"error": "Token not valid"}
    # checking if the user is not authorized, meaning that is not logged in or is a secretary
    if username not in users.keys() or token.split('-')[0] == "secretary":
        return {"error": "Authorization Error"}
    return ""

def validate_push_job(data):
    # checking if all data needed for posting a job was provided by the client
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "no token provided"}
    if "job_id" not in data:
        return {"error": "no job_id provided"}
    return ""


class Jobs_Queue(Resource):
    def post(self):
        validation = validate_push_job(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_append_pull(data["username"],
                                                          data["token"])  # check if the user has permission
        if validation != "":
            return validation

        job = fetch_job(data["job_id"])
        queue_jobs.put(job)

    def delete(self):
        pass




class Results_Queue(Resource):
    def post(self):
        pass































