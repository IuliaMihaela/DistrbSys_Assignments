from requests import put, get, post, delete
import json
# from rest_client_authentication import token
from services.authentication_service import users
# Master Data Service
# Jobs

token = users["felicity"]

print("post")
print("token:", token)
r = post('http://localhost:5001/jobs/api', json={'username': 'felicity', 'token': token, "timestamp": "15-04-2022 15:54", "status": "done", "date_range": "13-15", "assets": "1,2,3,4,5,11"})
job_response = json.loads(r.content.decode())
print(job_response)
job_id = job_response["message_body"]["id"]

print("get")
r = get('http://localhost:5001/jobs/api', json={'username':'felicity', 'token': token, "job_id": job_id})
job_response = json.loads(r.content.decode())
print(job_response)

print("put")
r = put('http://localhost:5001/jobs/api', json={"job_id": job_id, 'username': 'felicity', 'token': token, "timestamp": "13-04-2022 22:51:12", "status": "submitted", "date_range": "13-16 Jan", "assets": "1,2,3,4,5,11"})
job_response = json.loads(r.content.decode())
print(job_response)

print("delete")
r = delete('http://localhost:5001/jobs/api', json={"job_id": job_id, 'username': 'felicity', 'token': token})
job_response = json.loads(r.content.decode())
print(job_response)

# Results

print("post")
r = post('http://localhost:5001/results/api', json={'username': 'felicity', 'token': token, "job_id": job_id, "timestamp": "15-04-2022 19:56", "assets": "1,22,3,4,5,11"})
result_response = json.loads(r.content.decode())
result_id = result_response["message_body"]["job_id"]

print("get")
r = get('http://localhost:5001/results/api', json={'username': 'felicity', 'token': token, "job_id": job_id})
result_response = json.loads(r.content.decode())
print(result_response)

print("put")
r = put('http://localhost:5001/results/api', json={"job_id": job_id, 'username': 'felicity', 'token': token, "timestamp": "13-04-2022 22:51:12", "assets": "1,22,3,4,5,11"})
result_response = json.loads(r.content.decode())
print(result_response)

print("delete")
r = delete('http://localhost:5001/results/api', json={"job_id": job_id, 'username': 'felicity', 'token': token})
result_response = json.loads(r.content.decode())
print(result_response)

