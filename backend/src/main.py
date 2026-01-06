from fastapi import FastAPI
from core.config import settings
from api.invoices import router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# Routers
app.include_router(router, tags=["Invoices"])





