from OCR.extraer_ocr import extraer_factura_backend

def process_invoice_img(img, filename: str | None = None):
    return extraer_factura_backend(img, filename)

