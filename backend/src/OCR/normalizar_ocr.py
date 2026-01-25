import csv
import os
import re
import datetime

# ============================================================
# 1) FUNCIONES DE NORMALIZACIÓN
# ============================================================

def normalizar_cuit(texto):

   # Extrae CUIT, devuelve formato XX-XXXXXXXX-X.

    if not texto:
        return ""

    digits = re.sub(r"\D", "", texto)

    if len(digits) == 11:
        return f"{digits[0:2]}-{digits[2:10]}-{digits[10]}"

    return texto.strip()


def normalizar_fecha(texto):

    # Convierte a DD/MM/AAAA

    if not texto:
        return ""

    texto = texto.strip()

    # buscar patrón fecha dentro del texto
    match = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", texto)
    if match:
        texto = match.group(0)

    formatos = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d"]

    for f in formatos:
        try:
            dt = datetime.datetime.strptime(texto, f)
            return dt.strftime("%d/%m/%Y")
        except:
            pass

    return texto


def normalizar_total(texto):

    if not texto:
        return ""

    # buscar número con coma decimal
    match = re.search(r"[\d\.\s]+,\d{2}", texto)
    if match:
        texto = match.group(0)

    t = texto.strip().replace(" ", "")
    t = t.replace(".", "").replace(",", ".")

    try:
        return f"{float(t):.2f}"
    except:
        return texto.strip()


def normalizar_razon(texto):

    if not texto:
        return ""

    t = texto.upper()

    t = re.sub(r"^[^A-Z0-9]+", "", t)
    t = re.sub(r"^(FR\.|IR\.|LR\.|_?\?)\s*", "", t)

    t = re.sub(r"COD\.?\s*\d+", "", t)

    matches = re.findall(r"[A-Z0-9ÁÉÍÓÚÜ][A-Z0-9ÁÉÍÓÚÜ ,.-]+", t)
    if not matches:
        return t.strip()

    razon_social = max(matches, key=len)

    # limpiar espacios redundantes
    razon_social = " ".join(razon_social.split())

    return razon_social



def normalizar_numero_factura(texto):

    # Extrae el número más largo (mejor heurística OCR).

    if not texto:
        return ""

    numeros = re.findall(r"\d+", texto)
    if not numeros:
        return texto.strip()

    # tomar el grupo más largo
    return max(numeros, key=len)


def normalizar_tipo_factura(texto):

    if not texto:
        return ""

    t = texto.upper()

    # eliminar COD y códigos numéricos
    t = re.sub(r"COD\.?\s*\d+", "", t)

    # ahora sí buscar letra
    match = re.search(r"[ABC]", t)
    return match.group(0) if match else ""

HEADERS_TABLA = [
    "producto",
    "servicio",
    "cantidad",
    "subtotal"
]

def normalizar_tabla_items(texto):

    # Convierte el string de items OCR en una lista de dicts con descripcion, cantidad y subtotal.

    if not texto:
        return []

    # Eliminar encabezados
    t = re.sub(
        r"producto\s*/?\s*servicio\s*cantidad\s*subtotal",
        "",
        texto,
        flags=re.IGNORECASE
    )

    # Limpiar espacios redundantes
    t = " ".join(t.split())

    # Detectar cada item por patrón: cantidad + subtotal al final

    pattern = r"(.+?)\s+(\d+)\s+\$?([\d\.,]+)(?=\s|$)"
    matches = re.findall(pattern, t)

    items = []
    for descripcion, cantidad, subtotal in matches:
        descripcion = descripcion.strip()
        try:
            cantidad = int(cantidad)
        except:
            cantidad = 0
        subtotal = subtotal.replace(".", "").replace(",", ".")
        try:
            subtotal = float(subtotal)
        except:
            subtotal = 0.0

        items.append({
            "descripcion": descripcion,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

    return items


# ============================================================
# 2) TABLA DE NORMALIZADORES
# ============================================================

NORMALIZADORES = {
    "cuit_emisor": normalizar_cuit,
    "fecha": normalizar_fecha,
    "total": normalizar_total,
    "razon_social": normalizar_razon,
    "numero_factura": normalizar_numero_factura,
    "tipo_factura": normalizar_tipo_factura,
    "tabla_items": normalizar_tabla_items
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
        print(f"No se encontró {ruta_in}")
        return

    filas_normalizadas = []

    with open(ruta_in, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            campo = row["campo"]
            texto_ocr = row.get("texto_ocr", "")

            if campo in NORMALIZADORES:
                texto_norm = NORMALIZADORES[campo](texto_ocr)
            else:
                texto_norm = texto_ocr.strip()

            row["texto_ocr_normalizado"] = texto_norm
            filas_normalizadas.append(row)

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

    print(f"Archivo normalizado generado: {ruta_out}")


# ============================================================
# 4) MAIN
# ============================================================

if __name__ == "__main__":
    normalizar_csv_validacion()
    print("✔ Normalización completada.")
