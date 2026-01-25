from OCR.pipeline_detectar_yolo_ocr import procesar_factura_img
from OCR.normalizar_ocr import NORMALIZADORES, normalizar_tabla_items


def extraer_factura_backend(img, image_id: str | None = None):

    resultado_raw = procesar_factura_img(img, image_id)

    salida = {}

    # Normalizar todos los campos
    for campo, datos in resultado_raw.items():
        texto_ocr = datos.get("texto_ocr", "") or ""
        if campo in NORMALIZADORES:
            salida[campo] = NORMALIZADORES[campo](texto_ocr)
        else:
            salida[campo] = texto_ocr.strip()

    # Procesar tabla_items
    tabla_items = salida.get("tabla_items")
    if not isinstance(tabla_items, list):
        if isinstance(tabla_items, str):
            tabla_items = normalizar_tabla_items(tabla_items)
        else:
            tabla_items = []

    return {
        "tipo_factura": salida.get("tipo_factura", ""),
        "razon_social": salida.get("razon_social", ""),
        "cuit_emisor": salida.get("cuit_emisor", ""),
        "numero_factura": salida.get("numero_factura", ""),
        "fecha": salida.get("fecha", ""),
        "tabla_items": tabla_items,
        "total": salida.get("total", 0.0),
    }
