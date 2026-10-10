import os
import sys
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows to prevent cp1256 charmap encoding crashes
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Self-heal sys.path so 'app' imports work reliably from any working directory
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from app.config import settings
from app.core.database import init_db, engine
from app.models.db_models import StaffRecord, ScheduleActivity, MaterialLogRecord
from app.core.rag_engine import rag_engine
from app.routers.chat import router as chat_router
from app.routers.actions import router as actions_router
from app.routers.documents import router as documents_router
from app.routers.voice import router as voice_router
from app.routers.auth import router as auth_router
from app.api.v1.projects import router as projects_router
from app.api.v1.reports import router as reports_router
from app.api.v1.vision import router as vision_router
from app.api.v1.integrations import router as integrations_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.claims import router as claims_router
from app.api.v1.finance import router as finance_router
from app.api.v1.simulation import router as simulation_router
from app.api.v1.portfolio import router as portfolio_router
from app.routers.settings import router as settings_router

STATIC_DIR = Path(__file__).resolve().parent / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and populate ChromaDB RAG index
    print("[*] Initializing Smart Assistant Database & ChromaDB...")
    init_db()
    
    # Sync SQLite initial records into ChromaDB
    try:
        with Session(engine) as session:
            staff = session.exec(select(StaffRecord)).all()
            schedule = session.exec(select(ScheduleActivity)).all()
            materials = session.exec(select(MaterialLogRecord)).all()
            rag_engine.sync_records_to_chroma(staff, schedule, materials)
        print("[OK] Vector indexing and database ready.")
    except Exception as e:
        print(f"Chroma sync warning: {e}")
        
    yield
    print("Shutting down Smart Assistant Backend.")

app = FastAPI(
    title=settings.APP_NAME,
    description="Cross-platform AI Assistant Backend for Construction & Engineering Project Managers (Desktop, Mobile & Web)",
    version="1.0.0",
    lifespan=lifespan
)

# Restrict CORS to explicit allowlist
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Register API Routers (Mount under both /api/v1 and /api for seamless web client routing)
for api_prefix in [settings.API_V1_STR, "/api"]:
    app.include_router(auth_router, prefix=api_prefix)
    app.include_router(chat_router, prefix=api_prefix)
    app.include_router(actions_router, prefix=api_prefix)
    app.include_router(documents_router, prefix=api_prefix)
    app.include_router(voice_router, prefix=api_prefix)
    app.include_router(projects_router, prefix=api_prefix)
    app.include_router(reports_router, prefix=api_prefix)
    app.include_router(vision_router, prefix=api_prefix)
    app.include_router(integrations_router, prefix=api_prefix)
    app.include_router(alerts_router, prefix=api_prefix)
    app.include_router(claims_router, prefix=api_prefix)
    app.include_router(finance_router, prefix=api_prefix)
    app.include_router(simulation_router, prefix=api_prefix)
    app.include_router(portfolio_router, prefix=api_prefix)
    app.include_router(settings_router, prefix=api_prefix)

# Mount static files for Web Client
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "name": settings.APP_NAME,
        "status": "Online",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }

@app.get("/app")
def get_web_app():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Web client index.html not found"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Smart Assistant Backend"}

@app.post("/api/agent/hardware")
async def agent_hardware_heartbeat(request: Request):
    """Accepts periodic hardware heartbeat posts from external monitoring agents (prevents 404 log spam)."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
