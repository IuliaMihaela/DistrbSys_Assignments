from requests import put, get, post, delete
import datetime
import json




r = post('http://localhost:5000/users/registration/api/felicity', json={'password':"felicity12", 'role':'manager'})
print(r.json())

r = put('http://localhost:5000/users/login/api', json={'username':'felicity', 'password':"felicity12"})
print(r.json())

login_data = r.json()
token = login_data["felicity"]["token"]

r = post('http://localhost:5000/jobs/api', json={'username': 'felicity', 'token': token, "timestamp": "15-04-2022 15:54", "status": "done", "date_range": "13-15", "assets": "1,2,3,4,5,11"})
# job_data = r.json()
# job_id = list(job_data)[0]
# print(r.content)
job_response = json.loads(r.content.decode())
job_id = job_response["message_body"]["id"]

r = get('http://localhost:5000/jobs/api', json={'username':'felicity', 'token': token, "job_id": job_id})
job_response = json.loads(r.content.decode())
print(job_response)

r = put('http://localhost:5000/jobs/api', json={"job_id": job_id, 'username': 'felicity', 'token': token, "timestamp": "13-04-2022 22:51:12", "status": "submitted", "date_range": "13-16 Jan", "assets": "1,2,3,4,5,11"})
job_response = json.loads(r.content.decode())
print(job_response)

r = delete('http://localhost:5000/jobs/api', json={"job_id": job_id, 'username': 'felicity', 'token': token})
job_response = json.loads(r.content.decode())
print(job_response)

