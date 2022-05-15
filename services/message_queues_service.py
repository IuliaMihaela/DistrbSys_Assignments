import queue
from flask import request
from flask_restful import Resource
from master_data_service import *
from authentication_service import *
import uuid

# from services import api2, db2


queue_results = queue.Queue()



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


class handling_job_queues(Resource):
    def __init__(self, list_of_queues):
        self.list_of_queues = []

    def create(self, queue_name):
        data = request.json
        validation = validate_user_permission_delete_create(data["username"],
                                                            data["token"])  # check if the user has permission
        if validation != "":
            return validation

        # check if queue already exists
        if queue_name in self.list_of_queues:
            return {"error": "queue " + queue_name + " already exists"}
        else:
            queue_name = queue.Queue()
            self.list_of_queues.append(queue_name)



    def delete(self,queue_name):
        data = request.json
        validation = validate_user_permission_delete_create(data["username"],
                                                            data["token"])  # check if the user has permission
        if validation != "":
            return validation

        #if queue not in list
        if queue_name not in self.list_of_queues:
            return {"error": "queue " + queue_name + " not in list"}

        # deleting messages in queue
        with queue_name.mutex:
            queue_name.queue.clear()

        # deleting queue from list
        self.list_of_queues.remove(queue_name)

    def Listing(self):
        data = request.json

        # listing queue
        return self.list_of_queues


queue_jobs = handling_job_queues.create("queue_jobs")
print(queue_jobs.queue)

class Jobs_Queue(Resource):

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

        # push into the results queue
        queue_results.put(job_pulled)


        return "pulled ", job_pulled






        # have to send contents to caller




###################results#############################

def validate_result(data):
    # checking if all data needed for posting or updating a result was provided by the client
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


class Results_Queue(Resource):

    def push(self):
        validation = validate_result(request.json)  # check if all data was provided
        if validation != "":
            return validation

        data = request.json
        validation = validate_user_permission_append_pull_push(data["username"],
                                                               data["token"])  # check if the user has permission
        if validation != "":
            return validation

        result = fetch_result(data["job_id"])
        queue_results.put(result)

    def pull(self):
        data = request.json
        validation = validate_user_permission_append_pull_push(data["username"],
                                                               data["token"])  # check if the user has permission
        if validation != "":
            return validation

        # check if queue is not empty
        if queue_results.empty() == True:
            return {"error": "results queue is empty"}

        result_pulled = queue_results.get()

        return "pulled", result_pulled
