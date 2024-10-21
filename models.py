from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import MetaData
from database import Base

metadata = MetaData(schema='plm')


class Part(Base):
    __tablename__ = 'parts'
    __table_args__ = {'schema': 'plm'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    drawing = relationship("Drawing", back_populates="parts")
    drawing_id = Column(Integer, ForeignKey('plm.drawings.id'))


class Drawing(Base):
    __tablename__ = 'drawings'
    __table_args__ = {'schema': 'plm'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parts = relationship("Part", back_populates="drawing")

