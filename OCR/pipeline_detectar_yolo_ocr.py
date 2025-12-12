from detectar_recortar_ROIs import detectar_recortar_roi
from lector_ocr import ocr_roi

def procesar_factura(imagen_path):
    """
    Pipeline completo:
    - Detecta campos con YOLO
    - Recorta ROIs
    - Aplica OCR a cada ROI
    - Devuelve JSON con datos preliminares
    """
    print("\n=== Iniciando detección ===")
    detecciones = detectar_recortar_roi(imagen_path)

    resultado = {}

    for campo, info in detecciones.items():
        texto = ocr_roi(info["roi_path"])
        resultado[campo] = {
            "texto_ocr": texto,
            "confianza": info["conf"],
            "bbox": info["bbox"]
        }

    return resultado


if __name__ == "__main__":
    ejemplo = "./facturas_prueba/factura1.png"
    datos = procesar_factura(ejemplo)
    print("\nResultado OCR preliminar:\n")
    for k, v in datos.items():
        print(k, " => ", v)
