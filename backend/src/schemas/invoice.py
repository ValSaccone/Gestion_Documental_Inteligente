from pydantic import BaseModel
from typing import List
from datetime import date

class ItemCreate(BaseModel):
    descripcion: str
    cantidad: int
    precio_unitario: float

class InvoiceCreate(BaseModel):
    numero: str
    fecha: date | None
    tipo_factura: str | None
    total: float

    proveedor_id: int
    usuario_id: int

    detalles: List[ItemCreate]


class ItemResponse(BaseModel):
    descripcion: str
    cantidad: int
    precio_unitario: float

    class Config:
        from_attributes = True


class ProveedorResponse(BaseModel):
    nombre: str
    cuit: str
    direccion: str

    class Config:
        from_attributes = True

class InvoiceResponse(BaseModel):
    id: int
    numero: str
    fecha: date | None
    tipo_factura: str | None
    total: float

    proveedor: ProveedorResponse
    detalles: List[ItemResponse]

    class Config:
        from_attributes = True
