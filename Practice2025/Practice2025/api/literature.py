from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Source, SourceType
from typing import List

router = APIRouter()

class SourceBase(BaseModel):
    type_id: int
    name: str
    authors: str
    public_title: str
    publisher: str
    published_at: int
    published_where: str
    pages_count: int
    text_type_1: str
    text_type_2: str
    text_type_3: str

class SourceResponse(SourceBase):
    id: int

    class Config:
        from_attributes = True

def get_db():
    from config import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sources/", response_model=List[SourceResponse])
def get_sources(db: Session = Depends(get_db)):
    sources = db.query(Source).all()
    return sources