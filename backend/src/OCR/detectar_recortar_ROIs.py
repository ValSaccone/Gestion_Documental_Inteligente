import cv2
from ultralytics import YOLO
from pathlib import Path

# ==============================
# MODELO
# ==============================

#BASE_DIR = Path(__file__).resolve().parent

#PROJECT_ROOT = BASE_DIR.parents[2]

#MODEL_PATH = PROJECT_ROOT / "runs" / "models" / "model_yolo8n_v4_best.pt"


BASE_DIR = Path(__file__).resolve().parent  # backend/src/OCR
MODEL_PATH = BASE_DIR.parent / "runs" / "models" / "model_yolo8n_v4_best.pt"


print("Ruta del modelo probado:", MODEL_PATH)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Modelo no encontrado en {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))

# ==============================
# DEBUG ROIS
# ==============================
TEMP_ROI_DIR = BASE_DIR / "temp_rois"
TEMP_ROI_DIR.mkdir(exist_ok=True)

# ==============================
# CLASES
# ==============================
CLASSES = [
    "tipo_factura",
    "razon_social",
    "cuit_emisor",
    "numero_factura",
    "fecha",
    "tabla_items",
    "total"
]

# ==============================
def expandir_roi(x1, y1, x2, y2, img, px=15):
    h, w = img.shape[:2]
    return (
        max(0, x1 - px),
        max(0, y1 - px),
        min(w, x2 + px),
        min(h, y2 + px),
    )

# ==============================
def detectar_recortar_roi_img(img, image_id):
    results = model(img, conf=0.25)[0]
    detecciones = {}

    for i, box in enumerate(results.boxes):
        cls_id = int(box.cls[0])
        class_name = CLASSES[cls_id]
        conf = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

        # Ajustes por campo
        if class_name in ["cuit_emisor", "total"]:
            x1, y1, x2, y2 = expandir_roi(x1, y1, x2, y2, img, px=20)


        elif class_name == "tipo_factura":
            h, w = img.shape[:2]
            x1 = max(0, x1 - 5)
            x2 = min(w, x2 + 5)
            y1 = max(0, y1 - 25)
            y2 = max(y1 + 20, y2 - 30)

        elif class_name == "tabla_items":
            y1 = min(img.shape[0], y1 + 30)  # sacar títulos

        roi = img[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        # ==============================
        # GUARDAR ROIs
        # ==============================
        roi_name = f"{image_id}_{class_name}_{i}_{int(conf*100)}.png"
        cv2.imwrite(
            str(TEMP_ROI_DIR / roi_name),
            roi
        )

        detecciones[class_name] = {
            "bbox": [x1, y1, x2, y2],
            "conf": conf,
            "roi": roi
        }

    return detecciones

