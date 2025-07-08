from fastapi import FastAPI
from api import projects, files

app = FastAPI()

app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(files.router, prefix="/api/files", tags=["Files"])