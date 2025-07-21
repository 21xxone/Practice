# seed_data.py
from sqlalchemy.exc import IntegrityError
from config import get_db
from models import (
    ProjectType, Project, File,
    SourceType, Source
)

def seed_data():
    db = next(get_db())

    # ProjectType
    pt = db.query(ProjectType).filter_by(id=1).first()
    if not pt:
        pt = ProjectType(id=1, name="Default")
        db.add(pt)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            pt = db.query(ProjectType).filter_by(id=1).one()

    # Project
    proj = db.query(Project).filter_by(id=1).first()
    if not proj:
        proj = Project(
            id=1,
            name="Test Project",
            type_id=pt.id,
            author="Tester",
            tags="test,example",
            year=2025
        )
        db.add(proj)
        db.commit()

    # File
    f = db.query(File).filter_by(id=1).first()
    if not f:
        f = File(
            id=1,
            name="test.txt",
            path=f"files/{proj.id}/test.txt"
        )
        db.add(f)
        db.commit()

    # связь через relationship
    if f not in proj.files:
        proj.files.append(f)
        db.commit()

    # SourceType
    st = db.query(SourceType).filter_by(id=1).first()
    if not st:
        st = SourceType(id=1, name="Book")
        db.add(st)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            st = db.query(SourceType).filter_by(id=1).one()

    # Source
    src = db.query(Source).filter_by(id=1).first()
    if not src:
        src = Source(
            id=1,
            type_id=st.id,
            title="Example Book",
            authors="Ivanov I.I.",
            published_in="Journal XYZ",
            year=2025,
            pages=123,
            text_type_1="Lorem ipsum",
            text_type_2="Dolor sit amet",
            text_type_3="Consectetur"
        )
        db.add(src)
        db.commit()

if __name__ == "__main__":
    seed_data()
