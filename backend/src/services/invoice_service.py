from sqlalchemy.orm import Session
from models.factura import Factura
from models.proveedor import Proveedor
from models.detalle_factura import DetalleFactura

def factura_to_response(factura):
    return {
        "id": factura.id,
        "invoiceNumber": factura.numero,
        "date": factura.fecha,
        "total": factura.total,
        "provider": factura.proveedor.nombre,
        "providerCuit": factura.proveedor.cuit,
        "providerAddress": factura.proveedor.direccion,
        "items": [
            {
                "description": d.descripcion,
                "quantity": d.cantidad,
                "unitPrice": d.precio_unitario
            }
            for d in factura.detalles
        ]
    }


def create_invoice(db: Session, data: dict):
    proveedor = (
        db.query(Proveedor)
        .filter(Proveedor.cuit == data["providerCuit"])
        .first()
    )

    if not proveedor:
        proveedor = Proveedor(
            nombre=data["provider"],
            cuit=data["providerCuit"],
            direccion=data["providerAddress"]
        )
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)

    factura = Factura(
        numero=data["invoiceNumber"],
        total=data["total"],
        proveedor_id=proveedor.id
    )

    db.add(factura)
    db.commit()
    db.refresh(factura)

    for item in data["items"]:
        detalle = DetalleFactura(
            descripcion=item["description"],
            cantidad=item["quantity"],
            precio_unitario=item["unitPrice"],
            factura_id=factura.id
        )
        db.add(detalle)

    db.commit()
    return factura

