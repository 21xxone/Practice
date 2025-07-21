# api/projects.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from config import get_db
from models import Project, ProjectType
from schemas import ProjectBase, ProjectCreate, ProjectTypeBase

router = APIRouter()

@router.get("/types", response_model=List[ProjectTypeBase])
def get_project_types(db: Session = Depends(get_db)):
    return db.query(ProjectType).all()

@router.get("/", response_model=List[ProjectBase])
def get_projects(
    id: Optional[int]           = Query(None),
    type_id: Optional[int]      = Query(None),
    name: Optional[str]         = Query(None),
    author: Optional[str]       = Query(None),
    tags: Optional[str]         = Query(None),
    year: Optional[int]         = Query(None),
    created_from: Optional[datetime] = Query(None),
    created_to:   Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Project)
    if id is not None:      q = q.filter(Project.id == id)
    if type_id is not None: q = q.filter(Project.type_id == type_id)
    if name:                q = q.filter(Project.name.ilike(f"%{name}%"))
    if author:              q = q.filter(Project.author.ilike(f"%{author}%"))
    if tags:                q = q.filter(Project.tags.ilike(f"%{tags}%"))
    if year is not None:    q = q.filter(Project.year == year)
    if created_from:        q = q.filter(Project.created_at >= created_from)
    if created_to:          q = q.filter(Project.created_at <= created_to)
    return q.all()

@router.post("/", response_model=ProjectBase)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    pt = db.query(ProjectType).filter(ProjectType.id == project.type_id).first()
    if not pt:
        raise HTTPException(status_code=404, detail="ProjectType not found")
    db_proj = Project(**project.dict())
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj
