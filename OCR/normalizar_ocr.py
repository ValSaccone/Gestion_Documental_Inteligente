# OCR/normalizar_ocr.py

import csv
import os
import re
import datetime


# ============================================================
# 1) FUNCIONES DE NORMALIZACIÓN
# ============================================================

def normalizar_cuit(texto):
    """Convierte a formato XX-XXXXXXXX-X si tiene 11 dígitos."""
    digits = re.sub(r"\D", "", texto)
    if len(digits) == 11:
        return f"{digits[0:2]}-{digits[2:10]}-{digits[10]}"
    return texto.strip()


def normalizar_fecha(texto):
    """Convierte fechas a formato DD/MM/YYYY."""
    texto = texto.strip()
    formatos = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d"]

    for f in formatos:
        try:
            dt = datetime.datetime.strptime(texto, f)
            return dt.strftime("%d/%m/%Y")
        except:
            pass

    return texto


def normalizar_total(texto):
    """
    Normaliza montos con miles y decimales:
    Ejemplos:
       '129.067,54'  → '129067.54'
       '  67,40 '     → '67.40'
       '1 240,20'     → '1240.20'
    """
    t = texto.strip().replace(" ", "")

    # reemplazar miles y usar punto decimal
    t = t.replace(".", "").replace(",", ".")

    try:
        return f"{float(t):.2f}"
    except:
        return texto.strip()


def normalizar_razon(texto):
    """Elimina saltos de línea y espacios redundantes."""
    return " ".join(texto.replace("\n", " ").split())


def normalizar_numero_factura(texto):
    """Elimina espacios, puntos y ceros iniciales innecesarios."""
    t = re.sub(r"\D", "", texto)
    return t if t else texto.strip()


# ============================================================
# 2) TABLA DE NORMALIZADORES POR CAMPO
# ============================================================

NORMALIZADORES = {
    "cuit_emisor": normalizar_cuit,
    "fecha": normalizar_fecha,
    "total": normalizar_total,
    "razon_social": normalizar_razon,
    "numero_factura": normalizar_numero_factura
    # podés agregar más si necesitás
}


# ============================================================
# 3) PROCESAMIENTO DEL CSV DE VALIDACIÓN
# ============================================================

def normalizar_csv_validacion(
        entrada="validacion_ocr.csv",
        salida="validacion_ocr_normalizado.csv"
    ):

    ruta_in = os.path.join("./logs", entrada)
    ruta_out = os.path.join("./logs", salida)

    if not os.path.exists(ruta_in):
        print(f"❌ No se encontró {ruta_in}")
        return

    filas_normalizadas = []

    with open(ruta_in, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            campo = row["campo"]
            texto_ocr = row["texto_ocr"]

            # aplicar normalizador si existe
            if campo in NORMALIZADORES:
                texto_norm = NORMALIZADORES[campo](texto_ocr)
            else:
                texto_norm = texto_ocr.strip()

            row["texto_ocr_normalizado"] = texto_norm
            filas_normalizadas.append(row)

    # escribir archivo nuevo
    with open(ruta_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "factura", "campo",
            "texto_ocr", "texto_ocr_normalizado",
            "texto_esperado", "correcto"
        ])

        for r in filas_normalizadas:
            writer.writerow([
                r["factura"],
                r["campo"],
                r["texto_ocr"],
                r["texto_ocr_normalizado"],
                r["texto_esperado"],
                r["correcto"]
            ])

    print(f"📄 Archivo normalizado generado: {ruta_out}")


# ============================================================
# 4) EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":
    normalizar_csv_validacion()
    print("✔ Normalización completada.")
