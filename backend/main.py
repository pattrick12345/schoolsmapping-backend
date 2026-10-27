"""Lab 8 API. Run: uvicorn main:app --reload"""
import os
import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = Path(os.getenv('SCHOOLS_DB', str(Path(__file__).resolve().parent / 'school_directory.db')))
app = FastAPI(title='Thai Schools API - Lab 8')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173', 'https://schoolsmapping-frontend.onrender.com'], allow_credentials=False, allow_methods=['GET'], allow_headers=['*'])

def connect():
    db=sqlite3.connect(DB_PATH)
    db.row_factory=sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    return db

@app.get('/')
def home():
    return {'message':'Thai Schools API', 'docs':'/docs'}

@app.get('/provinces')
def provinces():
    with connect() as db:
        return [dict(r) for r in db.execute('SELECT id, name_th, name_en FROM provinces ORDER BY name_th')]

@app.get('/districts')
def districts(province_id: int = Query(...)):
    with connect() as db:
        return [dict(r) for r in db.execute('SELECT id, province_id, name_th, name_en FROM districts WHERE province_id=? ORDER BY name_th', (province_id,))]

@app.get('/subdistricts')
def subdistricts(district_id: int = Query(...)):
    with connect() as db:
        return [dict(r) for r in db.execute('SELECT id, district_id, name_th, name_en FROM subdistricts WHERE district_id=? ORDER BY name_th', (district_id,))]

@app.get('/schools')
def schools(keyword: str = '', province_id: int | None = None, district_id: int | None = None, subdistrict_id: int | None = None, limit: int = Query(20,ge=1,le=100), offset: int = Query(0,ge=0)):
    conditions=[];params=[]
    if keyword.strip():
        conditions.append('(name_th LIKE ? OR name_en LIKE ?)')
        val=f'%{keyword.strip()}%';params.extend([val,val])
    for col,value in [('province_id',province_id),('district_id',district_id),('subdistrict_id',subdistrict_id)]:
        if value is not None:conditions.append(f'{col}=?');params.append(value)
    where=(' WHERE ' + ' AND '.join(conditions)) if conditions else ''
    with connect() as db:
        total=db.execute('SELECT COUNT(*) FROM schools'+where,params).fetchone()[0]
        records=[dict(row) for row in db.execute('SELECT id, smis_code, name_th, name_en, province_id, district_id, subdistrict_id, province_name_th, district_name_th, subdistrict_name_th FROM schools'+where+' ORDER BY id LIMIT ? OFFSET ?', [*params,limit,offset])]
    return {'items':records,'total':total,'limit':limit,'offset':offset}

@app.get('/schools/{school_id}')
def school_detail(school_id: int):
    with connect() as db:
        row=db.execute('SELECT * FROM schools WHERE id=?',(school_id,)).fetchone()
        if row is None:raise HTTPException(status_code=404,detail='School not found')
        return dict(row)

@app.get('/schools/{school_id}/location')
def school_location(school_id: int):
    with connect() as db:
        row = db.execute('SELECT latitude, longitude FROM schools WHERE id=?', (school_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail='School not found')

        lat, lng = row['latitude'], row['longitude']
        if lat is None or lng is None:
            raise HTTPException(status_code=404, detail='School location unavailable')

        if not (5 <= lat <= 21 and 97 <= lng <= 106):
            raise HTTPException(status_code=404, detail='School location unavailable')

        return dict(row)