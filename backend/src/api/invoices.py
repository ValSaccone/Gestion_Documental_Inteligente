from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import numpy as np
import cv2

from db.session import get_db
from services.ocr_service import process_invoice_img
from services.invoice_service import create_invoice, factura_to_response
from schemas.invoice import InvoiceResponse, InvoiceCreate
from models import Factura

from PIL import Image
from pdf2image import convert_from_bytes
import io

#Router
router = APIRouter(prefix="/facturas")

@router.post("/upload")
async def upload_factura(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename.lower()

    # --- Convertir PDF o JPG/JPEG a PNG ---
    if filename.endswith((".jpg", ".jpeg")):
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        contents = buf.getvalue()
    elif filename.endswith(".pdf"):
        try:
            pages = convert_from_bytes(contents, dpi=300)
            pil_img = pages[0].convert("RGB")
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
            contents = buf.getvalue()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al procesar PDF: {str(e)}")

    img = cv2.imdecode(
        np.frombuffer(contents, np.uint8),
        cv2.IMREAD_COLOR
    )

    if img is None:
        raise HTTPException(status_code=400, detail="Imagen inválida")

    resultado = process_invoice_img(img, file.filename)

    tabla_items_list = resultado.get("tabla_items", [])

    return {
        "tipo_factura": resultado.get("tipo_factura", ""),
        "razon_social": resultado.get("razon_social", ""),
        "cuit_emisor": resultado.get("cuit_emisor", ""),
        "numero_factura": resultado.get("numero_factura", ""),
        "fecha": resultado.get("fecha", ""),
        "tabla_items": tabla_items_list,
        "total": resultado.get("total", 0.0),
    }
@router.post("/", response_model=InvoiceResponse, status_code=201)
def create_invoice_endpoint(
    data: InvoiceCreate,
    db: Session = Depends(get_db)
):
    factura = create_invoice(db, data.dict())
    return factura_to_response(factura)


@router.get("/", response_model=list[InvoiceResponse])
def list_invoices(db: Session = Depends(get_db)):
    facturas = db.query(Factura).all()
    return [factura_to_response(f) for f in facturas]


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == invoice_id).first()

    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    return factura_to_response(factura)


