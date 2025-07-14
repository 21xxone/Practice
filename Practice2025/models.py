from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProjectType(Base):
    __tablename__ = "project_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    projects = relationship("Project", back_populates="project_type")

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type_id = Column(Integer, ForeignKey("project_type.id"))
    author = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    tags = Column(String, nullable=True)
    year = Column(Integer, nullable=True)

    files = relationship("File", secondary="project_files", back_populates="projects")
    project_files = relationship("ProjectFile", back_populates="project", overlaps="files")
    project_type = relationship("ProjectType", back_populates="projects")

class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Убрано unique=True
    path = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    projects = relationship("Project", secondary="project_files", back_populates="files", overlaps="project_files")
    project_files = relationship("ProjectFile", back_populates="file", overlaps="projects,files")

class ProjectFile(Base):
    __tablename__ = "project_files"

    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
    file_id = Column(Integer, ForeignKey("file.id"), primary_key=True)

    project = relationship("Project", back_populates="project_files", overlaps="files,projects")
    file = relationship("File", back_populates="project_files", overlaps="files,projects")

Project.project_files = relationship("ProjectFile", back_populates="project", overlaps="files")
File.project_files = relationship("ProjectFile", back_populates="file", overlaps="projects,files")

class SourceType(Base):
    __tablename__ = "source_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

    sources = relationship("Source", back_populates="source_type")

class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("source_type.id"))
    name = Column(String(255))
    authors = Column(String(255))
    public_title = Column(String(255))
    publisher = Column(String(255))
    published_at = Column(Integer)
    published_where = Column(String(255))
    pages_count = Column(Integer)
    text_type_1 = Column(String(255))
    text_type_2 = Column(String(255))
    text_type_3 = Column(String(255))

    source_type = relationship("SourceType", back_populates="sources")