from pydantic import BaseModel
from typing import List, Optional

class PartBase(BaseModel):
    name: str
    description: Optional[str] = None

class PartCreate(PartBase):
    pass

class Part(PartBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class DrawingBase(BaseModel):
    name: str

class DrawingCreate(DrawingBase):
    parts: List[int] = []

class Drawing(DrawingBase):
    id: Optional[int] = None
    class Config:
        from_attributes = True
