from requests import put, get, post

r = post('http://localhost:5000/users/registration/api/felicity', json={'password':"felicity12", 'role':'manager'})
print(r.json())

r = put('http://localhost:5000/users/login/api', json={'username':'felicity', 'password':"felicity12"})
print(r.json())

login_data = r.json()
token = login_data["felicity"]["token"]

r = post('http://localhost:5000/jobs/api', json={'username': 'felicity', 'token': token, "timestamp": "13-04-2022 22:51:12", "status": "done", "date_range" :"13-15", "assets": [1,2,3,4,5,11]})
print(r.json())
job_data = r.json()
job_id = list(job_data)[0]


r = get('http://localhost:5000/jobs/api', json={'username':'felicity', 'token': token, "job_id": job_id})
print(r.json())


r = put('http://localhost:5000/jobs/api', json={"job_id": job_id, 'username': 'felicity', 'token': token, "timestamp": "13-04-2022 22:51:12", "status": "submitted", "date_range": "13-16 Jan", "assets": [1,2,3,4,5,11]})
print(r.json())
