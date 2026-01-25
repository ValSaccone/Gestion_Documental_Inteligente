from pydantic import BaseModel, field_validator, model_validator
from typing import List
from datetime import datetime


class TablaItemCreate(BaseModel):
    descripcion: str
    cantidad: int
    subtotal: float

    @field_validator("descripcion")
    @classmethod
    def descripcion_no_vacia(cls, v):
        if not v or not v.strip():
            raise ValueError("La descripción no puede estar vacía")
        return v

    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, v):
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return v

    @field_validator("subtotal")
    @classmethod
    def subtotal_positivo(cls, v):
        if v < 0:
            raise ValueError("El subtotal no puede ser negativo")
        return v


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
    tabla_items: List[TablaItemCreate]
    total: float

    @field_validator("tipo_factura", "razon_social")
    @classmethod
    def string_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v

    @field_validator("cuit_emisor")
    @classmethod
    def cuit_valido(cls, v):
        if not v or not v.strip():
            raise ValueError("El CUIT no puede estar vacío")
        if not v.isdigit():
            raise ValueError("El CUIT debe contener solo números")
        if len(v) != 11:
            raise ValueError("El CUIT debe tener 11 dígitos")
        return v

    @field_validator("numero_factura")
    @classmethod
    def numero_factura_valido(cls, v):
        if not v or not v.strip():
            raise ValueError("El número de factura no puede estar vacío")
        if not v.isdigit():
            raise ValueError("El número de factura debe contener solo números")
        return v

    @field_validator("fecha")
    @classmethod
    def fecha_valida(cls, v):
        if not v or not v.strip():
            raise ValueError("La fecha no puede estar vacía")
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Formato de fecha inválido, se espera dd/mm/aaaa")
        return v

    @field_validator("tabla_items")
    @classmethod
    def tabla_no_vacia(cls, v):
        if not v or len(v) == 0:
            raise ValueError("La factura debe tener al menos un item")
        return v

    @field_validator("total")
    @classmethod
    def total_positivo(cls, v):
        if v < 0:
            raise ValueError("El total no puede ser negativo")
        return v

    # VALIDACIÓN CRUZADA
    @model_validator(mode="after")
    def validar_total(self):
        suma = sum(item.subtotal for item in self.tabla_items)
        if round(suma, 2) != round(self.total, 2):
            raise ValueError(
                f"El total ({self.total}) no coincide con la suma de subtotales ({suma})"
            )
        return self


class InvoiceResponse(BaseModel):
    id: int
    tipo_factura: str | None
    razon_social: str
    cuit_emisor: str
    numero_factura: str
    fecha: str | None
    tabla_items: List[TablaItemResponse]
    total: float

    class Config:
        from_attributes = True
