from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from services.ocr_service import process_invoice
from services.invoice_service import create_invoice
from schemas.invoice import InvoiceCreate
from models import Factura


#Router
router = APIRouter(prefix="/invoices")

@router.post("/process")
async def process_invoice_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    data = process_invoice(file_path)
    return data


@router.post("/")
def create_invoice_endpoint(
    data: InvoiceCreate,
    db: Session = Depends(get_db)
):
    return create_invoice(db, data.dict())

@router.get("/")
def list_invoices(db: Session = Depends(get_db)):
    return db.execute("SELECT * FROM facturas").fetchall()

@router.get("/{invoice_id}")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == invoice_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura
