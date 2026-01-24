from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base

class DetalleFactura(Base):
    __tablename__ = "detalle_factura"

    id = Column(Integer, primary_key=True)
    descripcion = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    factura_id = Column(Integer, ForeignKey("facturas.id"))
    factura = relationship("Factura", back_populates="detalles")
