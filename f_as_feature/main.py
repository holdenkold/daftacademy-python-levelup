from fastapi import Cookie, FastAPI, HTTPException,Depends, Request
from fastapi.responses import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import json
from functools import wraps
from hashlib import sha256
from jinja2 import Template, Environment, FileSystemLoader

app = FastAPI()
security = HTTPBasic()
app.secret_key = "dXNlcl9uYW1lOnBhc3N3b3Jk"
app.session_token = lambda username, password: sha256(bytes(f"{username}{password}{app.secret_key}", encoding='utf8')).hexdigest()

class Credentials:
	def __init__(self):
		with open("credentials.json", 'r') as data:
			self.__dict__ = json.load(data)

	def verify(self, login, password):
		return login == self.__dict__['login'] and password == self.__dict__['password']
	
	def get_session_token(self):
		return app.session_token(self.__dict__['login'], self.__dict__['password'])

	def get_user(self):
		return self.__dict__['login']

cr = Credentials()

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		request = kwargs['request']
		if 'session_token' in request.cookies and request.cookies['session_token'] == cr.get_session_token():
			return f(*args,**kwargs)
		else:
			raise HTTPException(401,'Not authorized access')
	return decorated_function

@app.get('/')
def root():
	return {"message" : "Hello sweety ^.^"}

@app.get('/welcome')
@login_required
def welcome(request : Request):
	file_loader = FileSystemLoader('templates')
	env = Environment(loader=file_loader)
	template = env.get_template('welcome.html')
	return template.render( user=cr.get_user())


@app.get('/login')
@app.post('/login')
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	if cr.verify(credentials.username, credentials.password):
		session_token = app.session_token(credentials.username, credentials.password)
		response.set_cookie(key="session_token",value=session_token)
		response.status_code = 302
		response.headers['Location'] = '/welcome'
		return response
	else:
		raise HTTPException(401,'Invalid credentials')


@app.get('/logout')
@app.post('/logout')
def logout(request : Request, response: Response):
	response.delete_cookie('session_token')
	response.status_code = 302
	response.headers['Location'] = '/'
	return response