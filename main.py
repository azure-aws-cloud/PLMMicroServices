from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from drawingmodel import DrawingModel
from part import Part, Drawing
from partmodel import PartModel

# from models import SessionLocal, PartModel, Part, DrawingModel, Drawing

app = FastAPI()

# Dependency to get the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Part
@app.post("/parts/", response_model=PartModel)
def create_part(part: PartModel, db: Session = Depends(get_db)):
    db_part = Part(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

# Update Part
@app.put("/parts/{part_id}", response_model=PartModel)
def update_part(part_id: int, part: PartModel, db: Session = Depends(get_db)):
    db_part = db.query(Part).filter(Part.part_id == part_id).first()
    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")

    for key, value in part.dict(exclude_unset=True).items():
        setattr(db_part, key, value)

    db.commit()
    db.refresh(db_part)
    return db_part

# Delete Part
@app.delete("/parts/{part_id}", response_model=dict)
def delete_part(part_id: int, db: Session = Depends(get_db)):
    db_part = db.query(Part).filter(Part.part_id == part_id).first()
    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")

    db.delete(db_part)
    db.commit()
    return {"detail": "Part deleted successfully"}

# Create Drawing
@app.post("/drawings/", response_model=DrawingModel)
def create_drawing(drawing: DrawingModel, db: Session = Depends(get_db)):
    db_drawing = Drawing(**drawing.dict())
    db.add(db_drawing)
    db.commit()
    db.refresh(db_drawing)
    return db_drawing

# Update Drawing
@app.put("/drawings/{drawing_id}", response_model=DrawingModel)
def update_drawing(drawing_id: int, drawing: DrawingModel, db: Session = Depends(get_db)):
    db_drawing = db.query(Drawing).filter(Drawing.drawing_id == drawing_id).first()
    if not db_drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")

    for key, value in drawing.dict(exclude_unset=True).items():
        setattr(db_drawing, key, value)

    db.commit()
    db.refresh(db_drawing)
    return db_drawing

# Delete Drawing
@app.delete("/drawings/{drawing_id}", response_model=dict)
def delete_drawing(drawing_id: int, db: Session = Depends(get_db)):
    db_drawing = db.query(Drawing).filter(Drawing.drawing_id == drawing_id).first()
    if not db_drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")

    db.delete(db_drawing)
    db.commit()
    return {"detail": "Drawing deleted successfully"}
