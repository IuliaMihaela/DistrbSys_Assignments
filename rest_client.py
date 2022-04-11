from requests import put, get, post

r = post('http://localhost:5000/users/registration/api/felicity', json={'password':"felicity12", 'role':'manager'})
print(r.json())

r = put('http://localhost:5000/users/login/api', json={'username':'felicity', 'password':"felicity12"})
print(r.json())