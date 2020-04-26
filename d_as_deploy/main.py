from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import Response, Request

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

@app.api_route(path="/method", methods=["GET", "POST", "PUT", "DELETE"])
def show_method(request: Request):
	return {"method": request.method}

@app.post('/patient')
def patient_post(patient : Patient):
	app.counter+=1
	app.patients[app.counter] = patient
	return {"id" : app.counter, "patient" : patient}

@app.get('/patient/{pk}', response_model=Patient)
def patient_get(pk: int):
	if pk in app.patients:
		return app.patients[pk]
	return Response(status_code = 204)	