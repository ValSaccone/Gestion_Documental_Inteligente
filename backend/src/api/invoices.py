from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from services.ocr_service import process_invoice
from schemas.invoice import InvoiceResponse, InvoiceCreate
from models import Factura, DetalleFactura


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

