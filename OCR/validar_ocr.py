# OCR/validar_ocr.py

import os
import csv
import cv2

from pipeline_detectar_yolo_ocr import procesar_factura_img
from normalizar_ocr import NORMALIZADORES


# ----------------------------------------
# 1) Guardar resultados
# ----------------------------------------

def guardar_validacion(resultados, filename="validacion_ocr.csv"):
    logs_dir = "./logs"
    os.makedirs(logs_dir, exist_ok=True)

    ruta_salida = os.path.join(logs_dir, filename)

    with open(ruta_salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "factura",
            "campo",
            "texto_ocr",
            "texto_ocr_normalizado",
            "texto_esperado",
            "texto_esperado_normalizado",
            "correcto"
        ])

        for r in resultados:
            writer.writerow([
                r["factura"],
                r["campo"],
                r["texto_ocr"],
                r["texto_ocr_normalizado"],
                r["texto_esperado"],
                r["texto_esperado_normalizado"],
                r["correcto"]
            ])

    print(f"📄 Archivo de validación guardado en: {ruta_salida}")


# ----------------------------------------
# 2) Valores esperados
# ----------------------------------------

VALORES_ESPERADOS = {
    "factura_A_0019.png": {
        "numero_factura": "90672257",
        "fecha": "03/01/2026",
        "cuit_emisor": "30-61504717-8",
        "razon_social": "TORRES LLC",
        "tipo_factura": "A",
        "tabla_items": "N/A",
        "total": "2.757,90"
    },
    "factura_B_0658.png": {
        "numero_factura": "79770129",
        "fecha": "01/01/2026",
        "cuit_emisor": "27-17440151-6",
        "razon_social": "LEIVA CARRIZO",
        "tipo_factura": "B",
        "tabla_items": "N/A",
        "total": "2.605,18"
    },
    "factura_C_0720.png": {
        "numero_factura": "08146836",
        "fecha": "05/01/2026",
        "cuit_emisor": "23-58091128-6",
        "razon_social": "DUARTE, SUAREZ AND MENDEZ",
        "tipo_factura": "C",
        "tabla_items": "N/A",
        "total": "5.620,69"
    }
}


# ----------------------------------------
# 3) Validación OCR + YOLO
# ----------------------------------------

def validar_facturas():
    carpeta = "./facturas_prueba/"
    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(".png")]

    resultados_log = []

    for archivo in archivos:
        print(f"\n🔎 Procesando {archivo}...")

        ruta = os.path.join(carpeta, archivo)
        img = cv2.imread(ruta)

        if img is None:
            print(f"❌ No se pudo leer la imagen: {ruta}")
            continue

        image_id = os.path.splitext(archivo)[0]
        resultado = procesar_factura_img(img, image_id)
        esperados = VALORES_ESPERADOS.get(archivo, {})

        for campo, datos in resultado.items():
            texto_ocr = datos.get("texto_ocr") or ""
            texto_esp = esperados.get(campo, "")

            # Normalización segura
            if campo in NORMALIZADORES:
                texto_ocr_norm = NORMALIZADORES[campo](texto_ocr)
                texto_esp_norm = NORMALIZADORES[campo](texto_esp)
            else:
                texto_ocr_norm = texto_ocr.strip()
                texto_esp_norm = texto_esp.strip()

            # Regla especial: tabla_items
            if campo == "tabla_items":
                correcto = texto_ocr_norm != ""
            # Regla especial: total (comparar decimal)
            elif campo == "total":
                correcto = texto_ocr_norm == texto_esp_norm
            else:
                correcto = texto_ocr_norm == texto_esp_norm

            resultados_log.append({
                "factura": archivo,
                "campo": campo,
                "texto_ocr": texto_ocr,
                "texto_ocr_normalizado": texto_ocr_norm,
                "texto_esperado": texto_esp,
                "texto_esperado_normalizado": texto_esp_norm,
                "correcto": correcto
            })

    guardar_validacion(resultados_log)


# ----------------------------------------
# 4) Main
# ----------------------------------------

if __name__ == "__main__":
    validar_facturas()
    print("\n✔ Validación completa")
