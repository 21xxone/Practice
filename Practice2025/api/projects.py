from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from config import SessionLocal
from models import Project, ProjectType
from typing import List

router = APIRouter()

class ProjectBase(BaseModel):
    name: str
    type_id: int
    author: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    type_name: str

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    project_type = db.query(ProjectType).filter(ProjectType.id == project.type_id).first()
    if not project_type:
        raise HTTPException(status_code=404, detail="Project type not found")
    
    db_project = Project(
        name=project.name,
        type_id=project.type_id,
        author=project.author,
        created_at=datetime.utcnow()
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return {
        "id": db_project.id,
        "name": db_project.name,
        "type_id": db_project.type_id,
        "type_name": project_type.name,
        "author": db_project.author,
        "created_at": db_project.created_at
    }

@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [{
        "id": p.id,
        "name": p.name,
        "type_id": p.type_id,
        "type_name": p.type.name,
        "author": p.author,
        "created_at": p.created_at
    } for p in projects]