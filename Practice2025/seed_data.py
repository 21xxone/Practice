from datetime import datetime
from config import SessionLocal
from models import Project, File, ProjectFile, SourceType, Source, ProjectType

def seed_data():
    db = SessionLocal()
    try:
        # Добавляем тестовый проект
        project = Project(
            name="Test Project 2",
            type_id=1,
            author="John Doe",
            tags="drawio,2025",
            year=2025,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        # Добавляем тестовый файл
        file = File(
            name="MnePohuy.drawio.html",
            path="C:\\NewPractice\\files\\2\\drawio.html",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(file)
        db.commit()
        db.refresh(file)

        # Связываем проект и файл
        project_file = ProjectFile(project_id=project.id, file_id=file.id)
        db.add(project_file)

        # Добавляем тип источника
        source_type = SourceType(name="Book")
        db.add(source_type)
        db.commit()
        db.refresh(source_type)

        project_type = ProjectType(id=1, name="Default")
        db.add(project_type)
        db.commit()

        # Добавляем тестовый источник
        source = Source(
            type_id=source_type.id,
            name="Introduction to AI",
            authors="John Doe, Jane Smith",
            public_title="AI Basics",
            publisher="Tech Press",
            published_at=2023,
            published_where="New York",
            pages_count=300,
            text_type_1="Educational",
            text_type_2="Technical",
            text_type_3="Beginner"
        )
        db.add(source)
        db.commit()

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()