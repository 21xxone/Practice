from sqlalchemy.orm import Session
from config import SessionLocal
from models import ProjectType

def seed_data():
    db = SessionLocal()
    try:
        types = [
            ProjectType(name="Web Application"),
            ProjectType(name="Mobile App"),
            ProjectType(name="Data Analysis")
        ]
        db.add_all(types)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()