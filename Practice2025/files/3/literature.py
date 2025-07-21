# api/literature.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from config import get_db
from models import Source, SourceType
from schemas import SourceBase, SourceCreate, SourceTypeBase

router = APIRouter()

@router.get("/types", response_model=List[SourceTypeBase])
def get_source_types(db: Session = Depends(get_db)):
    return db.query(SourceType).all()

@router.get("/sources", response_model=List[SourceBase])
@router.get("/sources/", response_model=List[SourceBase])
def get_sources(
    id:           Optional[int] = Query(None),
    type_id:      Optional[int] = Query(None),
    title:        Optional[str] = Query(None),
    authors:      Optional[str] = Query(None),
    published_in: Optional[str] = Query(None),
    year:         Optional[int] = Query(None),
    pages:        Optional[int] = Query(None),
    text1:        Optional[str] = Query(None, alias="text_type_1"),
    text2:        Optional[str] = Query(None, alias="text_type_2"),
    text3:        Optional[str] = Query(None, alias="text_type_3"),
    db: Session = Depends(get_db),
):
    q = db.query(Source)
    if id is not None:       q = q.filter(Source.id == id)
    if type_id is not None:  q = q.filter(Source.type_id == type_id)
    if title:                q = q.filter(Source.title.ilike(f"%{title}%"))
    if authors:              q = q.filter(Source.authors.ilike(f"%{authors}%"))
    if published_in:         q = q.filter(Source.published_in.ilike(f"%{published_in}%"))
    if year is not None:     q = q.filter(Source.year == year)
    if pages is not None:    q = q.filter(Source.pages == pages)
    if text1:                q = q.filter(Source.text_type_1.ilike(f"%{text1}%"))
    if text2:                q = q.filter(Source.text_type_2.ilike(f"%{text2}%"))
    if text3:                q = q.filter(Source.text_type_3.ilike(f"%{text3}%"))
    return q.all()

@router.post("/sources", response_model=SourceBase)
@router.post("/sources/", response_model=SourceBase)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    st = db.query(SourceType).filter(SourceType.id == source.type_id).first()
    if not st:
        raise HTTPException(status_code=404, detail="SourceType not found")
    db_src = Source(**source.dict())
    db.add(db_src)
    db.commit()
    db.refresh(db_src)
    return db_src
