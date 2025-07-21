# schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ProjectTypeBase(BaseModel):
    id:   int
    name: str

class ProjectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:         int
    name:       str
    type_id:    int
    author:     str
    tags:       Optional[str]
    year:       Optional[int]
    created_at: datetime
    updated_at: datetime
    project_type: Optional[ProjectTypeBase]

class ProjectCreate(BaseModel):
    name:    str
    type_id: int
    author:  str
    tags:    Optional[str]
    year:    Optional[int]

class FileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:         int
    name:       str
    path:       str
    created_at: datetime
    updated_at: datetime

class SourceTypeBase(BaseModel):
    id:   int
    name: str

class SourceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:           int
    type_id:      int
    title:        str
    authors:      str
    published_in: Optional[str]
    year:         Optional[int]
    pages:        Optional[int]
    text_type_1:  Optional[str]
    text_type_2:  Optional[str]
    text_type_3:  Optional[str]

class SourceCreate(BaseModel):
    type_id:      int
    title:        str
    authors:      str
    published_in: Optional[str] = None
    year:         Optional[int] = None
    pages:        Optional[int] = None
    text_type_1:  Optional[str] = None
    text_type_2:  Optional[str] = None
    text_type_3:  Optional[str] = None

class SourceRead(SourceCreate):
    id:         int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
