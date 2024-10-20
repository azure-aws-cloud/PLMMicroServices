from sqlalchemy import Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship, Mapped, mapped_column
from typing import List, Optional

from base import Base


# SQLAlchemy Part Model
class Part(Base):
    __tablename__ = 'Part'
    __table_args__ = {'schema': 'plm'}

    part_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    part_name: Mapped[str] = mapped_column(String, nullable=False)
    part_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    lifecycle_state: Mapped[str] = mapped_column(String, nullable=False)

    drawings: Mapped[List["Drawing"]] = relationship("Drawing", back_populates="part")



# SQLAlchemy Drawing Model
class Drawing(Base):
    __tablename__ = 'Drawing'
    __table_args__ = {'schema': 'plm'}

    drawing_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    approved_by: Mapped[Optional[str]] = mapped_column(String)
    drawing_title: Mapped[str] = mapped_column(String, nullable=False)
    part_id: Mapped[int] = mapped_column(Integer, ForeignKey('plm.Part.part_id'), nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)

    part: Mapped[Part] = relationship("Part", back_populates="drawings")