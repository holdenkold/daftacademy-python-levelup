from fastapi import FastAPI

app = FastAPI()

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