from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "ABNT Formatador"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"

    # Database
    DATABASE_URL: str = "sqlite:///./abnt.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Payment
    # IMPORTANTE: Sistema sempre usa API real do Mercado Pago
    # Sem credenciais válidas = erro (nunca gera QR Code genérico)
    MERCADOPAGO_ACCESS_TOKEN: str = ""
    MERCADOPAGO_PUBLIC_KEY: str = ""
    MERCADOPAGO_TEST_MODE: bool = True  # Set to False for production
    PAYMENT_DEV_MODE: bool = False  # Development mode (should be False for production)
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLIC_KEY: str = ""

    # Google Sheets Database
    GOOGLE_SHEETS_SPREADSHEET_ID: str = ""
    GOOGLE_SHEETS_CREDENTIALS_FILE: str = "google_credentials.json"

    # Pricing
    PRICE_PER_PAGE: float = 0.80

    # File Upload
    MAX_FILE_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: str = "docx,pdf"
    UPLOAD_DIR: str = "uploads/temp"
    PROCESSED_DIR: str = "uploads/processed"

    # File Cleanup
    FILE_RETENTION_HOURS: int = 24

    # ABNT Settings
    DEFAULT_FONT: str = "Times New Roman"
    DEFAULT_FONT_SIZE: int = 12
    DEFAULT_LINE_SPACING: float = 1.5

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
