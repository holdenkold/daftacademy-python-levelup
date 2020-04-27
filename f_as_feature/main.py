from fastapi import Cookie, FastAPI, HTTPException,Depends, Request
from fastapi.responses import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from functools import wraps
from hashlib import sha256
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
security = HTTPBasic()
app.secret_key = "dXNlcl9uYW1lOnBhc3N3b3Jk"
app.session_token = lambda username, password: sha256(bytes(f"{username}{password}{app.secret_key}", encoding='utf8')).hexdigest()
template = Jinja2Templates(directory="templates")
app.counter = -1
app.patients = dict()

class Patient(BaseModel):
	name: str
	surename: str

class PatientResponse(BaseModel):
	id : int = 0
	patient : Patient

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
	return template.TemplateResponse(name = 'welcome.html', context={"request":request,'user' : cr.get_user()})

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

@app.post('/logout')
def logout(request : Request, response: Response):
	response.delete_cookie('session_token')
	response.status_code = 302
	response.headers['Location'] = '/'
	return response

@app.post('/patient')
@login_required
def patient_post(patient : Patient, response: Response):
	app.counter+=1
	app.patients[app.counter] = patient
	response.headers['Location'] = f'/patient/{app.counter}'
	response.status_code=302
	return response

@app.get('/patient/')
@login_required
def patients_get(response: Response):
	if not len(app.patients):
		return Response(status_code = 204)	

	people = dict()
	for id, p in app.patients.items():
		people[f'id_{id}'] = p
	return people

@app.get('/patient/{pk}', response_model=Patient)
@login_required
def patient_get(response: Response, pk: int):
	if pk in app.patients:
		return app.patients[pk]
	return Response(status_code = 204)	

@app.delete('/patient/{pk}')
@login_required
def patient_delete(response: Response, pk: int):
	app.patients.pop(pk, None)
	response.headers["Location"]="/patient"
	return Response(status_code = 204)