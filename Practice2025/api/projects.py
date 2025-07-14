from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List  # Добавлен импорт List
from datetime import datetime
from config import SessionLocal
from models import Project, ProjectType

router = APIRouter()

class ProjectCreate(BaseModel):
    name: str
    type_id: int
    author: str
    tags: str | None = None
    year: int | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    type_id: int
    author: str
    created_at: datetime
    updated_at: datetime | None
    tags: str | None
    year: int | None

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
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        tags=project.tags,
        year=project.year
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects