# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.projects   import router as projects_router
from api.files      import router as files_router
from api.literature import router as literature_router

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(projects_router,   prefix="/api/projects",   tags=["projects"])
app.include_router(files_router,      prefix="/api/files",      tags=["files"])
app.include_router(literature_router, prefix="/api/literature", tags=["literature"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")
