import json
import os

from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
from models import Drawing
from fastapi.responses import JSONResponse

import psycopg2
from psycopg2 import OperationalError


# create / update tables
models.Base.metadata.create_all(bind=engine)

def job():
    print("==I am training data every saturday at 6 AM Europe CET")


@asynccontextmanager
async def lifespan(app:FastAPI):
    scheduler = BackgroundScheduler(timezone="Europe/Berlin")
    scheduler.add_job(job, 'cron', day_of_week='sat', hour=6, minute=0)
    scheduler.start()
    yield
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db_user = os.getenv('DB_USERNAME')
if db_user is None:
    db_user = 'rhushi'

db_pass = os.getenv('DB_PASSWORD')
if db_pass is None:
    db_pass = 123

db_host = os.getenv('DB_HOST')
if db_host is None:
    db_host = 'localhost'
    # on win wsl , use the command to get ip
    # ip addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
    # use this ip in db_host and in the database explorer to connect to postgres

db_port = os.getenv('DB_PORT')
if db_port is None:
    db_port = 5432

db_schema = os.getenv('DB_SCHEMA')
if db_schema is None:
    db_schema = 'postgres'


DATABASE_CONFIG = {
    "host": f"{db_host}",
    "database": f"{db_schema}",
    "user": f"{db_user}",
    "password": f"{db_pass}",
    "port": f"{db_port}",
}
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/parts/", response_model=schemas.Part)
def create_part(part: schemas.PartCreate, db: Session = Depends(get_db)):
    db_part = models.Part(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

@app.get("/parts/{part_id}", response_model=schemas.Drawing)
def read_part(part_id: int, db: Session = Depends(get_db)):
    db_part = db.query(models.Part).filter(models.Part.id == part_id).first()
    if db_part is None:
        raise HTTPException(status_code=404, detail="Drawing not found")
    return db_part
@app.post("/drawings/", response_model=schemas.Drawing)
def create_drawing(drawing: schemas.DrawingCreate, db: Session = Depends(get_db)):
    # dwg_dict = drawing.model_dump()
    # dwg_json_pretty = json.dumps(dwg_dict, indent=2)
    # print(dwg_json_pretty)

    # Drawing needs Parts, so create drawing and add parts to the drawing
    db_drawing:Drawing = models.Drawing(name=drawing.name)
    db.add(db_drawing)
    db.commit()
    db.refresh(db_drawing)

    for part_id in drawing.parts:
        db_part: models.Part = db.query(models.Part).filter(models.Part.id == part_id).first()
        # print(db_part)
        db_part.drawing_id = db_drawing.id
        db.add(db_part)

    db.add(db_drawing)
    db.commit()
    db.refresh(db_drawing)



    return db_drawing

@app.get("/drawings/{drawing_id}", response_model=schemas.Drawing)
def read_drawing(drawing_id: int, db: Session = Depends(get_db)):
    db_drawing = db.query(models.Drawing).filter(models.Drawing.id == drawing_id).first()
    if db_drawing is None:
        raise HTTPException(status_code=404, detail="Drawing not found")
    return db_drawing

@app.get("/healthz")
async def liveness_check():
    # This is a simple liveness check endpoint
    return JSONResponse(status_code=200, content={"status": "alive"})

@app.get("/")
async def main():
    # This is a simple liveness check endpoint
    return JSONResponse(status_code=200, content={"message": "Welcome to PLM Microservice in Python !!!"})

@app.get("/readyz")
async def readiness_check():
    # Readiness check to see if the database is up and running
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
        return JSONResponse(status_code=200, content={"status": "ready"})
    except OperationalError:
        return JSONResponse(status_code=500, content={"status": "database not ready"})
