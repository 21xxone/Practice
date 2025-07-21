# models.py
from sqlalchemy import (
    Column, Integer, String, DateTime, Text,
    ForeignKey, Table, func
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

project_files = Table(
    "project_files",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    Column("file_id",    Integer, ForeignKey("file.id"),    primary_key=True),
)

class ProjectType(Base):
    __tablename__ = "project_type"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    projects = relationship("Project", back_populates="project_type")

class Project(Base):
    __tablename__ = "project"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    type_id    = Column(Integer, ForeignKey("project_type.id"), nullable=False)
    author     = Column(String, nullable=False)
    tags       = Column(String, nullable=True)
    year       = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    project_type = relationship("ProjectType", back_populates="projects")
    files        = relationship("File", secondary=project_files, back_populates="projects")

class File(Base):
    __tablename__ = "file"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    path       = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    projects = relationship("Project", secondary=project_files, back_populates="files")

class SourceType(Base):
    __tablename__ = "source_type"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sources = relationship("Source", back_populates="source_type")

class Source(Base):
    __tablename__ = "source"
    id            = Column(Integer, primary_key=True, index=True)
    type_id       = Column(Integer, ForeignKey("source_type.id"), nullable=False)
    title         = Column(String, nullable=True)
    authors       = Column(String, nullable=True)
    published_in  = Column(String, nullable=True)
    year          = Column(Integer, nullable=True)
    pages         = Column(Integer, nullable=True)
    text_type_1   = Column(Text, nullable=True)
    text_type_2   = Column(Text, nullable=True)
    text_type_3   = Column(Text, nullable=True)
    created_at    = Column(DateTime, server_default=func.now())
    updated_at    = Column(DateTime, server_default=func.now(), onupdate=func.now())

    source_type = relationship("SourceType", back_populates="sources")
