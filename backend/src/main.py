from fastapi import FastAPI
from core.config import settings
from db.session import Base, engine
from api.invoices import router

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# Routers
app.include_router(router, prefix="/invoices", tags=["Invoices"])





