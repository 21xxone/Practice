from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from config import SessionLocal, FILES_DIR
from models import File, ProjectFile, Project
from typing import List
import os

router = APIRouter()

class FileBase(BaseModel):
    name: str
    project_id: int

class FileCreate(BaseModel):
    project_id: int

class FileResponse(BaseModel):
    id: int
    name: str
    project_id: int | None
    path: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload", response_model=List[FileResponse])
async def upload_files(project_id: int, files: List[UploadFile] = FastAPIFile(...), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_dir = os.path.join(FILES_DIR, str(project_id))
    if not os.path.exists(project_dir):
        os.makedirs(project_dir, exist_ok=True)
    
    response = []
    for file in files:
        existing_file = db.query(File).join(ProjectFile).filter(
            File.name == file.filename,
            ProjectFile.project_id == project_id
        ).first()
        
        file_path = os.path.join(project_dir, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        if existing_file:
            existing_file.updated_at = datetime.utcnow()
            existing_file.path = file_path
            db_file = existing_file
        else:
            db_file = File(
                name=file.filename,
                path=file_path,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            
            project_file = ProjectFile(project_id=project_id, file_id=db_file.id)
            db.add(project_file)
        
        db.commit()
        db.refresh(db_file)
        
        response.append({
            "id": db_file.id,
            "name": db_file.name,
            "project_id": project_id,
            "path": db_file.path,
            "created_at": db_file.created_at,
            "updated_at": db_file.updated_at
        })
    
    return response

@router.get("/", response_model=List[FileResponse])
def get_files(db: Session = Depends(get_db)):
    files = db.query(File).all()
    return [
        {
            "id": f.id,
            "name": f.name,
            "project_id": f.project_files[0].project_id if f.project_files else None,
            "path": f.path,
            "created_at": f.created_at,
            "updated_at": f.updated_at
        }
        for f in files
    ]

@router.get("/search_by_project/{project_id}", response_model=List[FileResponse])
def search_files_by_project(project_id: int, tags: str = None, year: int = None, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    query = db.query(File).join(ProjectFile).filter(ProjectFile.project_id == project_id)
    
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        query = query.join(Project).filter(
            Project.tags.ilike(any(f"%{tag}%" for tag in tag_list))
        )
    
    if year:
        query = query.join(Project).filter(Project.year == year)
    
    files = query.all()
    if not files:
        raise HTTPException(status_code=404, detail="No files found for this project with given filters")
    
    return [
        {
            "id": f.id,
            "name": f.name,
            "project_id": project_id,
            "path": f.path,
            "created_at": f.created_at,
            "updated_at": f.updated_at
        }
        for f in files
    ]