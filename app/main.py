from fastapi import FastAPI
from app.base.config import settings
from app.db.database import test_database_connection

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API Raízes do Nordeste.",
)

@app.get("/", tags=["Geral"])
def root():
    return {
        "message": "Backend está em execução.",
        "version": settings.APP_VERSION,
    }

@app.get("/health", tags=["Monitoramento"])
def health():
    return {"status ok"}

@app.get("/health/database", tags=["Monitoramento"])
def database_health():
    test_database_connection()
    return {"status ok", "database connected"}
