# api/files.py

import os
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File as UploadFileField, Depends, HTTPException, Query
from fastapi.responses import FileResponse as StarletteFileResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc

from config import get_db, FILES_DIR
from models import File, Project
from schemas import FileResponse as FileSchema

router = APIRouter()

@router.post("/upload", response_model=List[FileSchema])
async def upload_files(
    project_id: int,
    files: List[UploadFile] = UploadFileField(...),
    db: Session = Depends(get_db),
):
    proj = db.query(Project).get(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    dest = os.path.join(FILES_DIR, str(project_id))
    os.makedirs(dest, exist_ok=True)

    saved_files: List[File] = []
    for up in files:
        path = os.path.join(dest, up.filename)
        with open(path, "wb") as f:
            f.write(await up.read())

        existing = (
            db.query(File)
            .filter(
                File.name == up.filename,
                File.projects.any(Project.id == project_id)
            )
            .first()
        )
        if existing:
            existing.path = path
            db.commit()
            db.refresh(existing)
            saved_files.append(existing)
        else:
            new_file = File(name=up.filename, path=path)
            db.add(new_file)
            db.commit()
            db.refresh(new_file)

            proj.files.append(new_file)
            db.commit()

            saved_files.append(new_file)

    return saved_files

@router.get("/", response_model=List[FileSchema])
def list_files(
    id: Optional[int] = Query(None, description="Фильтр по ID файла"),
    project_id: Optional[int] = Query(None, description="Фильтр по ID проекта"),
    db: Session = Depends(get_db),
):
    q = db.query(File)
    if id is not None:
        q = q.filter(File.id == id)
    if project_id is not None:
        q = q.join(File.projects).filter(Project.id == project_id)
    q = q.order_by(asc(File.id))
    return q.all()

@router.get("/search_by_project/{project_id}", response_model=List[FileSchema])
def search_by_project(
    project_id: int,
    tags: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    proj = db.query(Project).get(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    if tags and proj.tags and tags not in proj.tags:
        return []
    if year is not None and proj.year != year:
        return []
    return proj.files

@router.get("/download/{file_id}", response_class=StarletteFileResponse)
def download_file(file_id: int, db: Session = Depends(get_db)):
    file_obj = db.query(File).get(file_id)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found")
    return StarletteFileResponse(path=file_obj.path, filename=file_obj.name)
