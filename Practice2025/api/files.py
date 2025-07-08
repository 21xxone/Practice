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
    project_id: int
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
    
    response = []
    for file in files:
        # Проверяем, существует ли файл с таким именем для данного проекта
        existing_file = db.query(File).join(ProjectFile).filter(
            File.name == file.filename,
            ProjectFile.project_id == project_id
        ).first()
        
        # Формируем путь для сохранения
        file_path = os.path.join(FILES_DIR, file.filename)
        
        # Сохраняем содержимое файла
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        if existing_file:
            # Обновляем существующую запись
            existing_file.updated_at = datetime.utcnow()
            db_file = existing_file
        else:
            # Создаём новую запись
            db_file = File(
                name=file.filename,
                path=file_path,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            
            # Связываем файл с проектом
            project_file = ProjectFile(
                project_id=project_id,
                file_id=db_file.id
            )
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
    return [{
        "id": f.id,
        "name": f.name,
        "project_id": pf.project_id if (pf := f.project_links[0] if f.project_links else None) else None,
        "path": f.path,
        "created_at": f.created_at,
        "updated_at": f.updated_at
    } for f in files]