"""
FastAPI Application - ABNT Formatador
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .core.config import get_settings
from .api.routes import router

settings = get_settings()

# Cria aplicação
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para formatação automática de trabalhos acadêmicos seguindo normas ABNT",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra rotas
app.include_router(router, prefix="/api", tags=["documents"])


@app.on_event("startup")
async def startup_event():
    """Evento de inicialização."""
    # Cria diretórios necessários
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.PROCESSED_DIR, exist_ok=True)

    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} iniciado!")
    print(f"📝 Documentação: http://{settings.HOST}:{settings.PORT}/api/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de finalização."""
    print(f"👋 {settings.APP_NAME} finalizado")


@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
