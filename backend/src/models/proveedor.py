from sqlalchemy import Column, Integer, String
from .base import Base

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True)
    razon_social = Column(String, nullable=False)
    cuit_emisor = Column(String, unique=True, nullable=False)


