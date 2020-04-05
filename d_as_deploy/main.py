from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
app.counter = -1
app.patients = dict()

class Patient(BaseModel):
	name: str
	surname: str

class Response(BaseModel):
	id : int = 0
	patient : Patient

@app.get('/')
def hello_world():
	return {"message" : "Hello World during the coronavirus pandemic!"}

@app.get('/method')
def method_get():
	return {"method": "GET"}

@app.post('/method')
def method_post():
	return {"method": "POST"}

@app.put('/method')
def method_put():
	return {"method": "PUT"}

@app.delete('/method')
def method_delete():
	return {"method": "DELETE"}

@app.post('/patient', response_model = Response)
def patient_post(recieved : Patient):
	app.counter+=1
	app.patients[app.counter] = Patient
	return Response(id = app.counter, patient = recieved)

@app.get('/patient/{pk}', response_model=Patient)
def patient_get(pk: int):
	try:
		return app.patients[pk]
	except:
		raise HTTPException(204,"No such patient!")