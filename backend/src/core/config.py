from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Backend Gestion Documental"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql+psycopg2://admin:admin123@localhost:5432/gestion_documental_db"

    class Config:
        env_file = ".env"       # Busca el .env en la misma carpeta que este archivo
        env_file_encoding = "utf-8"

# Instancia de configuración
settings = Settings()


