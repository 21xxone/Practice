from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class ProjectType(Base):
    __tablename__ = 'project_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type_id = Column(Integer, ForeignKey('project_types.id'))
    author = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    type = relationship('ProjectType')
    files = relationship('ProjectFile', back_populates='project')

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)  # Путь к файлу в локальной папке
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project_links = relationship('ProjectFile', back_populates='file')

class ProjectFile(Base):
    __tablename__ = 'project_files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    file_id = Column(Integer, ForeignKey('file.id'))

    project = relationship('Project', back_populates='files')
    file = relationship('File', back_populates='project_links')