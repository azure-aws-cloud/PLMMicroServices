import json

from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
from models import Drawing

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

