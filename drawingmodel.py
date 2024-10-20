from pydantic import BaseModel
from typing import Optional

class DrawingModel(BaseModel):
    drawing_id: Optional[int] =None # Optional for creation
    approved_by: str
    drawing_title: str
    part_id: int  # This is required for creating a drawing
    state: str