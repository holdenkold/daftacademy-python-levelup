from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import Response

app = FastAPI()

@app.get('/')
def root():
	return {"message" : "Hello sweety ^.^"}

@app.get('/welcome')
def welcome():
	return {"message" : "Welcome sweety ^.^"}	