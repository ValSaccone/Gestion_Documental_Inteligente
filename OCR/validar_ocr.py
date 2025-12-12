# OCR/validar_ocr.py

import os
import csv
from pipeline_detectar_yolo_ocr import procesar_factura

# ----------------------------------------
# 1) Función para guardar resultados en CSV
# ----------------------------------------

def guardar_validacion(resultados, filename="validacion_ocr.csv"):
    logs_dir = "./logs"
    os.makedirs(logs_dir, exist_ok=True)

    ruta_salida = os.path.join(logs_dir, filename)

    escribir_encabezado = not os.path.exists(ruta_salida)

    with open(ruta_salida, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if escribir_encabezado:
            writer.writerow(["factura", "campo", "texto_ocr", "texto_esperado", "correcto"])

        for r in resultados:
            writer.writerow([
                r["factura"],
                r["campo"],
                r["texto_ocr"],
                r["texto_esperado"],
                r["correcto"]
            ])

    print(f"📄 Archivo de validación guardado en: {ruta_salida}")


# ----------------------------------------
# 2) Valores esperados (los completás vos)
# ----------------------------------------

VALORES_ESPERADOS = {

    "factura_A_0004.png": {
        "numero_factura": "95898083",
        "fecha": "26/06/2024",
        "cuit_emisor": "30-88429230-3",
        "razon_social": "Diaz-Benitez S.A.",
        "tipo_factura": "A",
        "tabla_items": "N/A",
        "total": "129.067,54",
        "qr": "N/A"
    },

    "factura_A_0018.png": {
        "numero_factura": "54364782",
        "fecha": "19/05/2024",
        "cuit_emisor": "24-75899328-0",
        "razon_social": "Gomez-Luna SRL",
        "tipo_factura": "A",
        "tabla_items": "N/A",
        "total": "102.460,40",
        "qr": "N/A"
    },

    "factura_A_0039.png": {
        "numero_factura": "23212703",
        "fecha": "19/11/2024",
        "cuit_emisor": "34-44392912-0",
        "razon_social": "Gutierrez and Sons SRL",
        "tipo_factura": "A",
        "tabla_items": "N/A",
        "total": "180.289,72",
        "qr": "N/A"
    },

    "factura_B_0668.png": {
        "numero_factura": "56735358",
        "fecha": "08/05/2025",
        "cuit_emisor": "27-98675762-8",
        "razon_social": "Cordoba, Gonzalez and Rios SRL",
        "tipo_factura": "B",
        "tabla_items": "N/A",
        "total": "115.039,63",
        "qr": "N/A"
    },

    "factura_B_0725.png": {
        "numero_factura": "87834161",
        "fecha": "31/05/2024",
        "cuit_emisor": "33-18420034-9",
        "razon_social": "Castillo-Acosta S.A.",
        "tipo_factura": "B",
        "tabla_items": "N/A",
        "total": "71.086,18",
        "qr": "N/A"
    },

    "factura_B_0737.png": {
        "numero_factura": "36024141",
        "fecha": "08/03/2025",
        "cuit_emisor": "33-43890163-7",
        "razon_social": "Blanco-Ramirez S.A.",
        "tipo_factura": "B",
        "tabla_items": "N/A",
        "total": "200.755,29",
        "qr": "N/A"
    },

    "factura_C_0922.png": {
        "numero_factura": "00513451",
        "fecha": "27/07/2025",
        "cuit_emisor": "20-55322589-2",
        "razon_social": "Maidana Inc SRL",
        "tipo_factura": "C",
        "tabla_items": "N/A",
        "total": "74.098,55",
        "qr": "N/A"
    },

    "factura_C_0935.png": {
        "numero_factura": "47638359",
        "fecha": "08/11/2025",
        "cuit_emisor": "27-73909312-8",
        "razon_social": "Cordoba-Soto S.R.L.",
        "tipo_factura": "C",
        "tabla_items": "N/A",
        "total": "19.605,30",
        "qr": "N/A"
    },

    "factura_A_0950.png": {
        "numero_factura": "27752257",
        "fecha": "30/04/2024",
        "cuit_emisor": "23-79261065-5",
        "razon_social": "Arias, Garcia and Silva SRL",
        "tipo_factura": "C",
        "tabla_items": "N/A",
        "total": "21.094,73",
        "qr": "N/A"
    },

    "Ticket_Comun_ticket_0466.png": {
        "numero_factura": "3998",
        "fecha": "24/05/2025",
        "cuit_emisor": "23-14827617-0",
        "razon_social": "PANADERÍA LA NUEVA",
        "tipo_factura": "N/A",      # No es factura A/B/C
        "tabla_items": "N/A",
        "total": "154.290,85",
        "qr": "N/A"
    },

    "Ticket_Comun_ticket_0475.png": {
        "numero_factura": "4901",
        "fecha": "25/04/2025",
        "cuit_emisor": "24-17584085-9",
        "razon_social": "SUPERMERCADO LOS ANDES",
        "tipo_factura": "N/A",
        "tabla_items": "N/A",
        "total": "117.182,56",
        "qr": "N/A"
    },

    "Ticket_Comun_ticket_0542.png": {
        "numero_factura": "2751",
        "fecha": "22/11/2025",
        "cuit_emisor": "23-51314930-5",
        "razon_social": "KIOSCO 24HS",
        "tipo_factura": "N/A",
        "tabla_items": "N/A",
        "total": "232.437,49",
        "qr": "N/A"
    }
}


# ----------------------------------------
# 3) Validación de facturas del lote
# ----------------------------------------

def validar_facturas():
    carpeta = "./facturas_prueba/"
    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(".png")]

    resultados_log = []

    for archivo in archivos:
        print(f"\n🔎 Procesando {archivo}...")

        ruta = os.path.join(carpeta, archivo)
        resultado = procesar_factura(ruta)

        esperados = VALORES_ESPERADOS.get(archivo, {})

        for campo, datos in resultado.items():
            texto_ocr = datos["texto_ocr"]
            texto_esp = esperados.get(campo, "")

            correcto = (texto_ocr.strip() == texto_esp.strip())

            resultados_log.append({
                "factura": archivo,
                "campo": campo,
                "texto_ocr": texto_ocr,
                "texto_esperado": texto_esp,
                "correcto": correcto
            })

    guardar_validacion(resultados_log)


# ----------------------------------------
# 4) Ejecución directa
# ----------------------------------------

if __name__ == "__main__":
    validar_facturas()
    print("\n✔ Validación completa")

