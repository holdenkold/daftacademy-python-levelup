import sqlite3
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel

class Album(BaseModel):
    title: str
    artist_id: int

class Customer(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None

app = FastAPI()

@app.on_event('startup')
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')    

@app.on_event('shutdown')
async def shutdown():
    app.db_connection.close()

@app.get('/')
def hello_world():
	return {'message' : 'Hello World!'}

# 1 part 
@app.get('/tracks')
async def get_tracks(page:int = 0, per_page:int = 10, status_code=200):
    app.db_connection.row_factory = sqlite3.Row
    tracks = app.db_connection.execute(f'SELECT * FROM tracks ORDER BY TrackId LIMIT {per_page * (page)}, {per_page}').fetchall()
    return tracks

# 2 part
@app.get('/tracks/composers')
async def get_composer_tracks(composer_name:str, status_code=200):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    tracks = app.db_connection.execute(f'SELECT name FROM tracks where composer = "{composer_name}" order by name').fetchall()
    if not tracks:
        return JSONResponse(status_code=404, content={'detail': {'error': f'No tracks for composer {composer_name}'}}) 
    return tracks
 
# 3 part
@app.post('/albums')
async def add_album(album:Album):
    app.db_connection.row_factory = sqlite3.Row
    cursor = app.db_connection.cursor()
    artist = cursor.execute(f'select name from artists where ArtistId = {album.artist_id}').fetchone()
    if artist:
        cursor.execute(f'insert into albums (Title, ArtistId) values ("{album.title}", {album.artist_id})')
        app.db_connection.commit()
        return JSONResponse(status_code=201, content = {'AlbumId' : cursor.lastrowid, 'Title' : album.title, 'ArtistId': album.artist_id})
    return JSONResponse(status_code=404, content={'detail': {'error': f'No artist with id: {album.artist_id}'}}) 

@app.get('/albums/{id}')
async def get_album_by_id(id:int, status_code=200):
    app.db_connection.row_factory = sqlite3.Row
    album = app.db_connection.execute(f'SELECT AlbumId, Title, ArtistId FROM albums where AlbumId = {id}').fetchone()
    if not album:
        return JSONResponse(status_code=404, content={'detail': {'error': f'No album with id: {id}'}}) 
    return album

# 4 part 
@app.put("/customers/{customer_id}")
async def edit_customer(customer:Customer, customer_id:int):
    app.db_connection.row_factory = sqlite3.Row
    cursor = app.db_connection.cursor()
    name = cursor.execute(f'select CustomerId from customers where CustomerId = {customer_id}').fetchone()
    if not name:
        return JSONResponse(status_code=404, content={'detail': {'error': f'No customer with id: {customer_id}'}}) 
    for k, v in customer.__dict__.items():
        if v:
            cursor.execute(f'update customers set {k} = "{v}" where CustomerId = {customer_id}')
            app.db_connection.commit()
    return cursor.execute(f'select * from customers where CustomerId={customer_id}').fetchone()

# 5/6 part 
@app.get('/sales')
async def get_statistics_by_category(category:str, status_code=200):
    app.db_connection.row_factory = sqlite3.Row
    if category == 'customers':
        data = app.db_connection.execute('''
        SELECT c.CustomerId, c.Email, c.Phone, round(sum(i.Total), 2) as Sum FROM customers as c
        JOIN invoices as i ON i.CustomerId = c.CustomerId
        group by c.CustomerId
        ORDER BY Sum DESC, c.CustomerId;
        ''').fetchall()
    elif category == 'genres':
        data = app.db_connection.execute('''
        SELECT g.Name, sum(ii.Quantity) as Sum FROM genres as g
        JOIN tracks as t ON t.GenreId = g.GenreId
        JOIN invoice_items as ii ON t.TrackId = ii.TrackId
        group by g.GenreId
        ORDER BY Sum DESC, g.Name;
        ''').fetchall()
    else:
        return JSONResponse(status_code=404, content={'detail': {'error': f'Unknown category'}}) 
    return data