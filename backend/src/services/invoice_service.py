from sqlalchemy.orm import Session
from models.factura import Factura
from models.proveedor import Proveedor
from models.detalle_factura import DetalleFactura
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from shared.errores import ServiceError, ResponseErrors


def factura_to_response(factura: Factura):
    return {
        "id": factura.id,
        "tipo_factura": factura.tipo_factura,
        "razon_social": factura.proveedor.razon_social,
        "cuit_emisor": factura.proveedor.cuit_emisor,
        "numero_factura": factura.numero_factura,
        "fecha": factura.fecha.strftime("%d/%m/%Y") if factura.fecha else None,
        "tabla_items": [
            {
                "descripcion": d.descripcion,
                "cantidad": d.cantidad,
                "subtotal": d.subtotal,
            }
            for d in factura.detalles
        ],
        "total": factura.total,
    }


def create_invoice(db: Session, data: dict):

    fecha_str = data.get("fecha")
    fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date() if fecha_str else None

    proveedor = (
        db.query(Proveedor)
        .filter(Proveedor.cuit_emisor == data["cuit_emisor"], Proveedor.razon_social == data["razon_social"])
        .first()
    )

    if not proveedor:
        proveedor = Proveedor(
            razon_social=data["razon_social"],
            cuit_emisor=data["cuit_emisor"]
        )
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)

    try:
        factura = Factura(
            numero_factura=data["numero_factura"],
            fecha=fecha,
            tipo_factura=data.get("tipo_factura"),
            total=data["total"],
            proveedor_id=proveedor.id
        )

        db.add(factura)
        db.commit()
        db.refresh(factura)

        for item in data.get("tabla_items", []):
            detalle = DetalleFactura(
                descripcion=item["descripcion"],
                cantidad=item["cantidad"],
                subtotal=item["subtotal"],
                factura_id=factura.id
            )
            db.add(detalle)

        db.commit()
        db.refresh(factura)

    except IntegrityError:
        db.rollback()
        raise ServiceError(ResponseErrors.DATOS_DUPLICADOS, "Factura duplicada")

    except Exception as e:
        db.rollback()
        raise ServiceError(ResponseErrors.ERROR_INTERNO, str(e))

    return factura
