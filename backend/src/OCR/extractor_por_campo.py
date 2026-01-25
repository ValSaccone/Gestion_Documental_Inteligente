import re

def extraer_por_campo(campo, texto):
    if not texto or texto == "UNREADABLE":
        return ""

    if campo == "numero_factura":
        nums = re.findall(r"\d{6,}", texto)
        return nums[-1] if nums else ""

    if campo == "fecha":
        m = re.search(r"\d{2}/\d{2}/\d{4}", texto)
        return m.group(0) if m else ""

    if campo == "cuit_emisor":
        m = re.search(r"\d{2}-\d{8}-\d", texto)
        return m.group(0) if m else ""

    if campo == "total":
        m = re.search(r"([\d\.]+,\d{2})", texto)
        return m.group(1) if m else ""

    if campo == "tipo_factura":
        m = re.search(r"\b[A-C]\b", texto)
        return m.group(0) if m else ""

    if campo == "razon_social":
        return texto.upper().strip()

    if campo == "tabla_items":
        return "N/A"

    return texto.strip()
