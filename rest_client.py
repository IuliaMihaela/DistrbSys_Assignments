from requests import put, get, post

# r = post('http://localhost:5000/users/registration/api/felicity', json={'password':"felicity12", 'role':'manager'})
# print(r.json())
#
# r = put('http://localhost:5000/users/login/api', json={'username':'felicity', 'password':"felicity12"})
# print(r.json())

r = post('http://localhost:5000/jobs/api', json={'username': 'felicity', 'token': "manager-87ef903f-bb63-11ec-9a15-44af28c6779f", "timestamp": "13-04-2022 22:51:12", "date_range":"13-15", "assets":[1,2,3,4,5,11]})





