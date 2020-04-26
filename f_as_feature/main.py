from fastapi import Cookie, FastAPI, HTTPException,Depends, Request
from fastapi.responses import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import json
from hashlib import sha256

class Credentials:
	def __init__(self):
		with open("credentials.json", 'r') as data:
			self.__dict__ = json.load(data)

	def verify(self, login, password):
		return login in self.__dict__['login'] and password in self.__dict__['password']

app = FastAPI()
security = HTTPBasic()
app.secret_key = "dXNlcl9uYW1lOnBhc3N3b3Jk"
cr = Credentials()

@app.get('/')
def root():
	return {"message" : "Hello sweety ^.^"}

@app.get('/welcome')
def welcome():
	return {"message" : "Welcome sweety ^.^"}	


@app.get('/login')
@app.post('/login')
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	if cr.verify(credentials.username, credentials.password):
		session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
		response.set_cookie(key="session_token",value=session_token)
		response.status_code = 302
		response.headers['Location'] = '/welcome'
		return response
	else:
		raise HTTPException(401,'Invalid credentials')


			
	