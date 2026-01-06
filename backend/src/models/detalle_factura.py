from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base

class DetalleFactura(Base):
    __tablename__ = "detalle_factura"

    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    cantidad = Column(Integer)
    precio_unitario = Column(Float)

    factura_id = Column(Integer, ForeignKey("facturas.id"))
    factura = relationship("Factura", back_populates="detalles")
