from datetime import date
from OCR.pipeline_detectar_yolo_ocr import procesar_factura_img

def process_invoice_img(img):
    return procesar_factura_img(img)


def process_invoice(file):
    """
    Este módulo actúa como wrapper del pipeline:
    - preprocesamiento
    - detección YOLO
    - OCR
    - extracción estructurada
    """
    # Ejemplo: acá llamás a TU código real
    extracted_data = {
        "invoiceNumber": "0001-00001234",
        "date": date(2024, 10, 12),
        "total": 15230.50,
        "tax": "21%",
        "provider": "Empresa S.A.",
        "providerCuit": "30-12345678-9",
        "providerAddress": "Av. Siempre Viva 123",
        "items": []
    }

    return extracted_data

