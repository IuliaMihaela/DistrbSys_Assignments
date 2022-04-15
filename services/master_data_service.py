from services.authentication_service import *
from services import api, db
from services.models import Job, Result


# Master Data Service

def create_response(message):
    #creating the response that is sent to the client
    return {
        "source": "http://127.0.0.1:5000",
        "destination": "client",
        "message_body": message
    }

####### Jobs ########

def validate_post_job(data):
    # checking if all data needed for posting a job was provided by the client
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
    # checking if all data needed for getting or deleting a job or a result was provided by the client
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "no token provided"}
    if "job_id" not in data:
        return {"error": "no job_id provided"}
    return ""

def validate_update_job(data):
    # checking if all data needed for updating a job was provided by the client
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
    # checking if the token is valid
    if token_state['success'] == False:
        return {"error": "Token not valid"}
    # checking if the user is not authorized, meaning that is not logged in or is a secretary
    if username not in users.keys() or token.split('-')[0] == "secretary":
        return {"error": "Authorization Error"}
    return ""


def create_job(data):
    # creating the id
    new_job_id = str(uuid.uuid1())
    # creating an instance of class Job
    new_job = Job(id=new_job_id, username=data['username'], timestamp=data['timestamp'], status=data['status'], date_range=data['date_range'], assets=data['assets'])
    db.session.add(new_job)  # add job to database
    db.session.commit()  # save changes to database
    return new_job.serialize()


def fetch_job(job_id):
    try:
        # get the job by id
        job = Job.query.get(job_id)
        return job.serialize()
    except:
        return "Job not found"

def update_job(data):
    # update all attributes of the job with the ones given by the user
    id = data['job_id']
    job = Job.query.get(id)
    job.username = data['username']
    job.timestamp = data['timestamp']
    job.status = data['status']
    job.date_range = data['date_range']
    job.assets = data['assets']
    db.session.commit() # save all changes to database
    return job.serialize()

def delete_job(job_id):
    try:
        # get the job by id
        job = Job.query.get(job_id)
        db.session.delete(job)  # delete job from database
        db.session.commit()  # save changes
        return {"success": True}
    except:
        return "Job not found"

class Jobs(Resource):
    def post(self):  # posting a new job
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

    def get(self):   # getting a job by id
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

    def put(self):  # updating a job
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

    def delete(self):  # deleting a job by id
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

####### Results ########

def validate_post_update_result(data):
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


def create_result(data):
    new_result = Result(job_id=data['job_id'], timestamp=data['timestamp'], assets=data['assets'])
    db.session.add(new_result)  # add job to database
    db.session.commit()  # save changes to database
    return new_result.serialize()

def fetch_result(job_id):
    try:
        # get result by the job id
        result = Result.query.get(job_id)
        return result.serialize()
    except:
        return "Result not found"

def update_result(data):
    id = data['job_id']
    # get result by the job id
    result = Result.query.get(id)
    # update all the attributes of the result with the ones given by the client
    result.timestamp = data['timestamp']
    result.assets = data['assets']
    db.session.commit()  # save changes
    return result.serialize()

def delete_result(job_id):
    try:
        # get result by the job id
        result = Result.query.get(job_id)
        db.session.delete(result)  # delete the result
        db.session.commit()  # save cahnges
        return {"success": True}
    except:
        return "Result not found"


class Results(Resource):
    def post(self):  # posting a new result
        validation = validate_post_update_result(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"],
                                                          data["token"])  # check if the user has permission
        if validation != "":
            return validation

        new_result = create_result(request.json)
        response = create_response(new_result)
        return response

    def get(self):  # getting a result by its job id
        validation = validate_get_delete_job_result(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"], data["token"])
        if validation != "":
            return validation
        result = fetch_result(data["job_id"])
        response = create_response(result)
        return response

    def put(self):  # updating a result
        validation = validate_post_update_result(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"], data["token"])
        if validation != "":
            return validation
        updated_result = update_result(request.json)
        response = create_response(updated_result)
        return response

    def delete(self):  # deleting a result by its job id
        validation = validate_get_delete_job_result(request.json)
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_master_data(data["username"], data["token"])
        if validation != "":
            return validation
        deleted_result_response = delete_result(data["job_id"])
        response = create_response(deleted_result_response)
        return response


api.add_resource(Jobs, '/jobs/api')
api.add_resource(Results, '/results/api')