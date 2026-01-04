from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class DetalleFactura(Base):
    __tablename__ = "detalle_factura"

    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    cantidad = Column(String)
    precio_unitario = Column(String)

    factura_id = Column(Integer, ForeignKey("facturas.id"))
    factura = relationship("Factura", back_populates="detalles")
