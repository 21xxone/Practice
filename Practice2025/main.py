from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import literature
from api.files import router as files_router
from api.projects import router as projects_router
from api.literature import router as literature_router

app = FastAPI()

# Добавление CORS для работы с фронтендом на порту 8001
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_router, prefix="/api/files", tags=["files"])
app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
app.include_router(literature_router, prefix="/api/literature", tags=["literature"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)