from sqlalchemy import Column, Integer, String
from .base import Base

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    cuit = Column(String, unique=True, nullable=False)
    direccion = Column(String)

