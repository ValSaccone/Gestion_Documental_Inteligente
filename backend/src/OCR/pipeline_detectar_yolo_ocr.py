import re
from OCR.detectar_recortar_ROIs import detectar_recortar_roi_img
from OCR.lector_ocr import ocr_roi

def extraer_tipo_factura(texto):
    texto = texto.upper()
    for t in ["A", "B", "C"]:
        if t in texto:
            return t
    return ""

def extraer_total(texto):
    m = re.search(r"(\d{1,3}(\.\d{3})*,\d{2})", texto)
    return m.group(1) if m else ""

def procesar_factura_img(img, image_id):

    detecciones = detectar_recortar_roi_img(img, image_id)
    resultado = {}

    for campo, info in detecciones.items():
        texto = ocr_roi(info["roi"])

        if campo == "tipo_factura":
            texto = extraer_tipo_factura(texto)

        if campo == "total":
            texto = extraer_total(texto)

        if not texto:
            texto = ""

        resultado[campo] = {
            "texto_ocr": texto,
            "conf": info["conf"],
            "bbox": info["bbox"]
        }

    return resultado
