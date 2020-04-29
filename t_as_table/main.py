import sqlite3
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.on_event('startup')
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')
    # app.cursor = app.db_connection.cursor()

@app.on_event('shutdown')
async def shutdown():
    app.db_connection.close()

@app.get('/')
def hello_world():
	return {'message' : 'Hello World!'}

@app.get('/tracks')
async def get_tracks(page:int = 0, per_page:int = 20, status_code=200):
    cursor = app.db_connection.cursor()
    query = f'SELECT name FROM tracks ORDER BY TrackId LIMIT {per_page * (page)}, {per_page * (page + 1)}'
    tracks = cursor.execute(query).fetchall()
    return { "tracks": tracks}

@app.get('/tracks/composers')
async def get_composer_tracks(composer_name:str, status_code=200):
    cursor = app.db_connection.cursor()
    query = f'SELECT name FROM tracks where composer = {composer_name} order by name'
    tracks = cursor.execute(query).fetchall() 
    return tracks