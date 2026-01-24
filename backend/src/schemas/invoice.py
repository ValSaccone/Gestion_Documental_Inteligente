from pydantic import BaseModel
from typing import List
from datetime import date

class TablaItemCreate(BaseModel):
    descripcion: str
    cantidad: int
    subtotal: float

class TablaItemResponse(BaseModel):
    descripcion: str
    cantidad: int
    subtotal: float

    class Config:
        from_attributes = True


class InvoiceCreate(BaseModel):
    tipo_factura: str
    razon_social: str
    cuit_emisor: str
    numero_factura: str
    fecha: str
    tabla_items: list[TablaItemCreate]
    total: float


class InvoiceResponse(BaseModel):
    id: int
    tipo_factura: str | None
    razon_social: str
    cuit_emisor: str
    numero_factura: str
    fecha: str | None
    tabla_items: list[TablaItemResponse]
    total: float

    class Config:
        from_attributes = True
