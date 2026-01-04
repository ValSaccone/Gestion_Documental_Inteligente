from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True)
    numero = Column(String, nullable=False)
    fecha = Column(Date)
    tipo_factura = Column(String)
    total = Column(String)

    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    proveedor = relationship("Proveedor")
    usuario = relationship("Usuario")
    detalles = relationship(
        "DetalleFactura",
        back_populates="factura",
        cascade="all, delete-orphan"
    )
