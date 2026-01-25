from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True)
    numero_factura = Column(String, unique=True, nullable=False)
    fecha = Column(Date)
    tipo_factura = Column(String)
    total = Column(Float)

    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))

    proveedor = relationship("Proveedor")
    detalles = relationship(
        "DetalleFactura",
        back_populates="factura",
        cascade="all, delete-orphan"
    )




