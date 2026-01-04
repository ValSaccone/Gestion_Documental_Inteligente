from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from db.session import get_db
from services.ocr_service import process_invoice
from services.invoice_service import create_invoice

router = APIRouter(prefix="/invoices", tags=["Invoices"])

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

@router.post("/confirm")
def confirm_invoice(data: dict, db: Session = Depends(get_db)):
    return create_invoice(db, data)

@router.get("/")
def list_invoices(db: Session = Depends(get_db)):
    return db.execute("SELECT * FROM facturas").fetchall()
