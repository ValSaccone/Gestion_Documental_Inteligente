from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from services.ocr_service import process_invoice
from schemas.invoice import InvoiceResponse, InvoiceCreate
from models import Factura, DetalleFactura
from fastapi import UploadFile, File, Depends
import numpy as np
import cv2
from services.ocr_service import process_invoice_img


#Router
router = APIRouter(prefix="/invoices")

@router.post("/process")
async def process_invoice_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    # Convertir bytes a imagen OpenCV
    img_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Imagen inválida")

    data = process_invoice_img(img)
    return data


@router.post(
    "/",
    response_model=InvoiceResponse,
    status_code=201
)
def create_invoice_endpoint(
    data: InvoiceCreate,
    db: Session = Depends(get_db)
):
    factura = Factura(
        numero=data.numero,
        fecha=data.fecha,
        tipo_factura=data.tipo_factura,
        total=data.total,
        proveedor_id=data.proveedor_id,
        usuario_id=data.usuario_id,
    )

    for item in data.detalles:
        factura.detalles.append(
            DetalleFactura(
                descripcion=item.descripcion,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario
            )
        )

    db.add(factura)
    db.commit()
    db.refresh(factura)

    return factura


@router.get("/", response_model=list[InvoiceResponse])
def list_invoices(db: Session = Depends(get_db)):
    return db.query(Factura).all()


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == invoice_id).first()

    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    return factura

