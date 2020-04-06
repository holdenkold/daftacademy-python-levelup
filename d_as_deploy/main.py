from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import Response

app = FastAPI()
app.counter = -1
app.patients = dict()

class Patient(BaseModel):
	name: str
	surename: str

class PatientResponse(BaseModel):
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

@app.post('/patient')
def patient_post(patient : Patient):
	app.counter+=1
	app.patients[app.counter] = patient
	return {"id" : app.counter, "patient" : patient}
	# return Response(id = app.counter, patient = recieved)

@app.get('/patient/{pk}', response_model=Patient)
def patient_get(pk: int):
	try:
		return app.patients[pk]
	except:
		return Response(status_code = 204)

	