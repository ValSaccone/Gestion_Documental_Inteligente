import os
import cv2
from ultralytics import YOLO

# Cargar modelo entrenado
MODEL_PATH = "../ML_module/models/model_yolo8n_v1_best.pt"
model = YOLO(MODEL_PATH)

# Carpeta para guardar ROIs recortados
TEMP_ROI_DIR = "./temp_rois"
os.makedirs(TEMP_ROI_DIR, exist_ok=True)

# Mapeo para nombres de clases
CLASSES = [
    "numero_factura",
    "fecha",
    "cuit_emisor",
    "razon_social",
    "tipo_factura",
    "tabla_items",
    "total",
    "qr"
]

def detectar_recortar_roi(imagen_path):
    """
    Detecta regiones en una factura usando YOLO y recorta cada ROI.
    Retorna un diccionario con paths de los recortes y coordenadas.
    """
    results = model(imagen_path)[0]
    img = cv2.imread(imagen_path)

    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {imagen_path}")

    detecciones = {}

    for box in results.boxes:
        cls_id = int(box.cls[0])
        class_name = CLASSES[cls_id]
        conf = float(box.conf[0])

        # Coordenadas
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

        # Recorte
        roi = img[y1:y2, x1:x2]
        roi_path = os.path.join(TEMP_ROI_DIR, f"{class_name}.png")

        cv2.imwrite(roi_path, roi)

        detecciones[class_name] = {
            "bbox": [x1, y1, x2, y2],
            "conf": conf,
            "roi_path": roi_path
        }

    return detecciones


if __name__ == "__main__":
    # Ejemplo de prueba
    imagen = "./facturas_prueba/factura1.png"
    out = detectar_recortar_roi(imagen)
    print(out)
