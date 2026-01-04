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
        "date": "2024-10-12",
        "total": "15230.50",
        "tax": "21%",
        "provider": "Empresa S.A.",
        "providerCuit": "30-12345678-9",
        "providerAddress": "Av. Siempre Viva 123",
        "items": []
    }

    return extracted_data


def process_invoice(file):
    """
    Wrapper del pipeline OCR ya desarrollado.
    """
    # Acá conectás tu código real
    return {
        "invoiceNumber": "0001-00001234",
        "date": "2024-10-12",
        "total": "15230.50",
        "tax": "21%",
        "provider": "Empresa S.A.",
        "providerCuit": "30-12345678-9",
        "providerAddress": "Av. Siempre Viva 123",
        "items": [
            {"description": "Producto A", "quantity": "2", "unitPrice": "1500"}
        ]
    }
