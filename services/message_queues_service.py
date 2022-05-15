
import queue
from flask import request
from flask_restful import Resource
from master_data_service import *
from authentication_service import *
import uuid

# from services import api2, db2


queue_results = queue.Queue()
queue_jobs = queue.Queue()


def validate_user_permission_append_pull_push(username, token):
    token_state = verify_token(username, token)
    # checking if the token is valid
    if token_state['success'] == False:
        return {"error": "Token not valid"}
    # checking if the user is not authorized, meaning that is not logged in or is a secretary
    if username not in users.keys() or token.split('-')[0] == "secretary":
        return {"error": "Authorization Error"}
    return ""


def validate_user_permission_delete_create(username, token):
    token_state = verify_token(username, token)
    # checking if the token is valid
    if token_state['success'] == False:
        return {"error": "Token not valid"}
    # checking if the user is not authorized, meaning that is not logged in or is not an administrator
    if username not in users.keys() or token.split('-')[0] != "administrator":
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

    def create(self,queue):
        list_of_queues = []
        data = request.json
        validation = validate_user_permission_delete_create(data["username"],
                                                               data["token"])  # check if the user has permission
        if validation != "":
            return validation

        # check if queue already exists

        if queue in list_of_queues:
            return {"error": "queue " + queue + " already exists"}
        else:
            list_of_queues.append(queue)

        return list_of_queues


    def push(self):
        validation = validate_push_job(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_append_pull_push(data["username"],
                                                               data["token"])  # check if the user has permission
        if validation != "":
            return validation

        job = fetch_job(data["job_id"])
        queue_jobs.put(job)

    def pull(self):
        data = request.json
        validation = validate_user_permission_append_pull_push(data["username"],
                                                               data["token"])  # check if the user has permission
        if validation != "":
            return validation

        # check if queue is not empty
        if queue_jobs.empty() == True:
            return {"error": "job queue is empty"}

        job_pulled = queue_jobs.get()
        return "pulled ", job_pulled

        # have to send contents to caller

    def Listing(self):
        data = request.json
        validation = validate_user_permission_append_pull_push(data["username"],
                                                               data["token"])  # check if the user has permission
        if validation != "":
            return validation

        # check if queue is not empty
        if queue_jobs.empty() == True:
            return {"error": "job queue is empty"}

        # listing queue
        return queue_jobs.queue

    def delete(self):
        data = request.json
        validation = validate_user_permission_delete_create(data["username"],
                                                               data["token"])  # check if the user has permission
        if validation != "":
            return validation

        # check if queue is not empty
        if queue_jobs.empty() == True:
            return {"error": "job queue is already empty"}

        # deleting queue
        with queue_jobs.mutex:
            queue_jobs.queue.clear()






class Results_Queue(Resource):
    def post(self):
        pass






























