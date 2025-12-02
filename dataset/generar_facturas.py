#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador sintético de facturas argentinas (A, B, C) y tickets comunes.
Produce PDFs, un annotations.json y archivos de anotación .txt en formato YOLO.
Optimizado para OCR y simulación de comprobantes reales AFIP.
"""

import os, json, random, datetime
from faker import Faker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black
from reportlab.lib.utils import ImageReader
import qrcode
from io import BytesIO

fake = Faker("es_AR")
OUTDIR = "facturas"
os.makedirs(OUTDIR, exist_ok=True)

TIPOS = {
    "A": os.path.join(OUTDIR, "Factura_A"),
    "B": os.path.join(OUTDIR, "Factura_B"),
    "C": os.path.join(OUTDIR, "Factura_C"),
    "TICKET": os.path.join(OUTDIR, "Ticket_Comun"),
}
for d in TIPOS.values():
    os.makedirs(d, exist_ok=True)

ANNOT_FILE = os.path.join(OUTDIR, "annotations.json")

# --- Configuración y Constantes YOLO ---
# YOLO classes map
YOLO_CLASS_MAP = {
    "numero_factura": 0,
    "fecha": 1,
    "cuit_emisor": 2,
    "razon_social": 3,
    "tipo_factura": 4,
    "tabla_items": 5,
    "total": 6,
    "qr": 7
}

# Dimensiones A4 en unidades ReportLab (points, donde 1pt = 1/72 inch)
# Para ReportLab, A4 es (595.2755905511812, 841.8897637795277)
WIDTH_PT, HEIGHT_PT = A4  # Ancho y alto en puntos (A4)


# Bounding box helper: convierte [x1, y1, x2, y2] de ReportLab (esquina inferior izquierda)
# a formato YOLO normalizado [cx, cy, w, h]
def bbox_to_yolo(box, img_w, img_h):
    x1, y1, x2, y2 = box

    # ReportLab Y es desde abajo. YOLO/Imágenes Y es desde arriba.
    # 1. Convertir Y1 (inferior) y Y2 (superior) a coordenadas de imagen (desde arriba)
    y1_img = img_h - y2  # La coordenada superior (Y2 de ReportLab) es la inferior de la imagen.
    y2_img = img_h - y1  # La coordenada inferior (Y1 de ReportLab) es la superior de la imagen.

    # 2. Calcular centro y dimensiones en puntos
    cx_pt = (x1 + x2) / 2.0
    cy_pt = (y1_img + y2_img) / 2.0
    w_pt = x2 - x1
    h_pt = y2_img - y1_img

    # 3. Normalizar a [0..1]
    cx = cx_pt / img_w
    cy = cy_pt / img_h
    w = w_pt / img_w
    h = h_pt / img_h

    return cx, cy, w, h


# -------------------- Helpers --------------------

def gen_cuit():
    pref = random.choice([20, 23, 24, 27, 30, 33, 34])
    mid = random.randint(10000000, 99999999)
    end = random.randint(0, 9)
    return f"{pref:02d}-{mid:08d}-{end}"


def gen_cae(): return "".join(str(random.randint(0, 9)) for _ in range(14))


def gen_pv(): return f"{random.randint(1, 9999):04d}"


def gen_comp_num(): return f"{random.randint(1, 99999999):08d}"


def format_money(v): return f"${v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gen_items(n=5):
    productos = [
        "Yerba Mate 1kg", "Pan Lactal", "Aceite de Girasol 900ml",
        "Harina 000 1kg", "Arroz largo fino 1kg",
        "Gaseosa Cola 2L", "Queso Cremoso 500g", "Leche Entera 1L",
        "Galletitas surtidas", "Azúcar 1kg", "Servicio técnico", "Baterías AA x4"
    ]
    items = []
    for _ in range(n):
        p = random.choice(productos)
        q = random.randint(1, 5)
        u = round(random.uniform(300, 15000), 2)
        st = round(q * u, 2)
        items.append({"cant": q, "desc": p, "unit": u, "subtotal": st})
    return items


def make_qr(data):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    bio = BytesIO();
    img.save(bio, format="PNG");
    bio.seek(0)
    return ImageReader(bio)


# -------------------- PDF DRAW + BBOX --------------------

def draw_factura(path, tipo, meta):
    width, height = A4
    c = canvas.Canvas(path, pagesize=A4)
    m = 20 * mm
    boxes = {}

    # Marco principal
    c.setStrokeColor(black)
    c.rect(m, m, width - 2 * m, height - 2 * m)

    # Recuadro con letra (tipo_factura)
    x_box = width / 2 - 10 * mm
    y_box = height - 35 * mm
    w_box = 20 * mm
    h_box = 20 * mm
    c.rect(x_box, y_box, w_box, h_box)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 22 * mm, tipo)
    # BBOX: ReportLab (x1, y1, x2, y2)
    boxes["tipo_factura"] = (x_box, y_box, x_box + w_box, y_box + h_box)

    # Encabezado empresa (razon_social)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(m + 5, height - 25 * mm, meta["emisor"]["razon_social"])
    c.setFont("Helvetica", 9)
    # BBOX: razon_social (cubre nombre y domicilio, aprox 20mm de alto)
    boxes["razon_social"] = (m + 5, height - 35 * mm - 2, m + 5 + 100 * mm, height - 25 * mm + 2)  # Ajuste manual

    # CUIT Emisor
    cuit_y = height - 30 * mm
    c.drawString(m + 5, cuit_y, f"CUIT: {meta['emisor']['cuit']}  |  IVA: {meta['emisor']['iva']}")
    c.drawString(m + 5, height - 35 * mm, f"Domicilio: {meta['emisor']['domicilio']}")
    # BBOX: cuit_emisor (solo la línea CUIT)
    boxes["cuit_emisor"] = (m + 5, cuit_y - 3, m + 5 + 80 * mm, cuit_y + 3)  # Asume 3mm de padding

    # Info factura (numero_factura, fecha)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(width - m - 5, height - 25 * mm, f"Factura {tipo}")

    # Número de factura (numero_factura)
    c.setFont("Courier", 10)
    nro_y = height - 30 * mm
    c.drawRightString(width - m - 5, nro_y, f"P.V: {meta['punto_venta']} N° {meta['nro']}")
    # BBOX: numero_factura (ajuste manual)
    boxes["numero_factura"] = (width - m - 70 * mm, nro_y - 3, width - m - 5, nro_y + 3)

    # Fecha (fecha)
    c.setFont("Helvetica", 9)
    fecha_y = height - 35 * mm
    c.drawRightString(width - m - 5, fecha_y, f"Fecha: {meta['fecha']}")
    # BBOX: fecha (ajuste manual)
    boxes["fecha"] = (width - m - 50 * mm, fecha_y - 3, width - m - 5, fecha_y + 3)

    # Receptor (no se pide bbox para receptor, solo para los del mapa)
    c.line(m + 5, height - 40 * mm, width - m - 5, height - 40 * mm)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(m + 5, height - 46 * mm, "Cliente:")
    c.setFont("Helvetica", 9)
    c.drawString(m + 35, height - 46 * mm, meta["receptor"]["nombre"])
    if meta["receptor"]["cuit"]:
        c.drawString(m + 35, height - 51 * mm, f"CUIT: {meta['receptor']['cuit']}")
    c.drawString(m + 35, height - 56 * mm, f"Condición frente al IVA: {meta['receptor']['iva']}")
    c.drawString(m + 35, height - 61 * mm, f"Condición de venta: {meta['cond_venta']}")

    # Tabla ítems (tabla_items)
    start_y = height - 80 * mm
    c.line(m + 5, start_y, width - m - 5, start_y)

    # Dibujo de ítems
    y = start_y - 28  # Posición inicial del primer item
    c.setFont("Helvetica", 9)
    y_start_items = y  # Coordenada Y (inferior) del primer item

    for it in meta["items"]:
        c.drawString(m + 8, y, str(it["cant"]))
        c.drawString(m + 40, y, it["desc"])
        c.drawRightString(width - m - 120, y, format_money(it["unit"]))
        c.drawRightString(width - m - 40, y, format_money(it["subtotal"]))
        y -= 14

    y_end_items = y + 14  # Coordenada Y (inferior) del último item

    # BBOX: tabla_items (incluye cabecera y todos los items)
    # y1: Posición inferior del último item (y_end_items - padding)
    # y2: Posición superior de la cabecera (start_y + padding)
    boxes["tabla_items"] = (m + 5, y_end_items - 14, width - m - 5, start_y + 5)

    # Totales (total)
    base = sum(i["subtotal"] for i in meta["items"])
    y_total_box = y  # Altura base antes de dibujar totales

    if tipo == "A":
        iva = round(base * 0.21, 2)
        total = round(base + iva, 2)
        c.drawRightString(width - m - 120, y - 10, "Subtotal:")
        c.drawRightString(width - m - 40, y - 10, format_money(base))
        c.drawRightString(width - m - 120, y - 25, "IVA 21%:")
        c.drawRightString(width - m - 40, y - 25, format_money(iva))
        y_total_draw = y - 45
    else:
        total = base
        c.setFont("Helvetica-Oblique", 8)
        c.drawRightString(width - m - 40, y - 15, "IVA incluido en el precio final")
        y_total_draw = y - 45

    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - m - 120, y_total_draw, "TOTAL:")
    c.drawRightString(width - m - 40, y_total_draw, format_money(total))

    # BBOX: total (cubre el valor total y el texto 'TOTAL:')
    boxes["total"] = (width - m - 130, y_total_draw - 5, width - m - 30, y_total_draw + 15)

    # Pie
    cae, vto = meta["CAE"], meta["CAE_vto"]
    c.setFont("Helvetica", 8)
    c.drawString(m + 5, 25 * mm, f"CAE: {cae}  |  Vto CAE: {vto}")

    # QR (qr)
    qr_x_coord = width - m - 90
    qr_y_coord = 15 * mm
    qr_size = 70
    qr = make_qr(meta["qr"])
    c.drawImage(qr, qr_x_coord, qr_y_coord, width=qr_size, height=qr_size)
    # BBOX: qr
    boxes["qr"] = (qr_x_coord, qr_y_coord, qr_x_coord + qr_size, qr_y_coord + qr_size)

    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(width / 2, 10 * mm, "Documento generado sintéticamente — No válido fiscalmente")
    c.save()

    # --- Generar líneas YOLO ---
    yolo_lines = []
    for key, box in boxes.items():
        cls_id = YOLO_CLASS_MAP.get(key, None)
        if cls_id is None:
            continue
        cx, cy, w, h = bbox_to_yolo(box, WIDTH_PT, HEIGHT_PT)
        yolo_lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

    return yolo_lines


# -------------------- Ticket Argentino Realista + BBOX --------------------

def draw_ticket(path, meta):
    width, height = A4
    c = canvas.Canvas(path, pagesize=A4)
    ticket_w = 80 * mm
    x0 = (width - ticket_w) / 2
    y = height - 40 * mm
    boxes = {}

    # Razon Social (razon_social)
    c.setFont("Courier-Bold", 10)
    c.drawCentredString(x0 + ticket_w / 2, y, meta["comercio"].upper())
    # BBOX: razon_social (cubre nombre y dirección, aprox 30mm)
    boxes["razon_social"] = (x0, y - 20, x0 + ticket_w, y + 10)  # 10pt arriba, 20pt abajo
    y -= 10

    # CUIT Emisor (cuit_emisor)
    c.setFont("Courier", 8)
    cuit_y = y
    c.drawCentredString(x0 + ticket_w / 2, cuit_y, f"CUIT: {meta['emisor']['cuit']} - IVA INSC.")
    # BBOX: cuit_emisor
    boxes["cuit_emisor"] = (x0, cuit_y - 5, x0 + ticket_w, cuit_y + 5)
    y -= 10

    c.drawCentredString(x0 + ticket_w / 2, y, meta["direccion"])
    y -= 10

    # Fecha + Nro Ticket (fecha, numero_factura)
    fn_y = y
    c.drawCentredString(x0 + ticket_w / 2, fn_y, f"Fecha: {meta['fecha']}  TICKET #{meta['nro']}")
    # BBOX: fecha y numero_factura (comparten la misma línea)
    boxes["fecha"] = (x0, fn_y - 5, x0 + ticket_w, fn_y + 5)
    boxes["numero_factura"] = boxes["fecha"]
    y -= 8

    c.line(x0, y, x0 + ticket_w, y)
    y -= 10

    # Items (tabla_items)
    y_start_items = y  # Coordenada Y (inferior) de la cabecera

    for it in meta["items"]:
        desc = it["desc"][:20]
        c.drawString(x0 + 2 * mm, y, f"{it['cant']}x {desc}")
        c.drawRightString(x0 + ticket_w - 2 * mm, y, format_money(it["subtotal"]))
        y -= 8

    y_end_items = y + 8  # Coordenada Y (inferior) del último item

    # BBOX: tabla_items (desde la cabecera hasta el último item)
    boxes["tabla_items"] = (x0 + 2 * mm, y_end_items - 8, x0 + ticket_w - 2 * mm,
                            y_start_items + 5)  # 5pt padding arriba/abajo

    y -= 6
    c.line(x0, y, x0 + ticket_w, y)

    # Total (total)
    total = sum(i["subtotal"] for i in meta["items"])
    y -= 12
    c.setFont("Courier-Bold", 9)
    total_y = y
    c.drawRightString(x0 + ticket_w - 2 * mm, total_y, f"TOTAL: {format_money(total)}")
    # BBOX: total
    boxes["total"] = (x0, total_y - 5, x0 + ticket_w, total_y + 15)
    y -= 10

    # Forma de pago (no se pide bbox)
    c.setFont("Courier", 8)
    c.drawString(x0 + 2 * mm, y, f"Forma de pago: {meta['pago']}")
    y -= 30

    # QR (qr)
    qr_x_coord = x0 + ticket_w / 2 - 25
    qr_y_coord = y - 50
    qr_size = 50
    qr = make_qr(meta["qr"])
    c.drawImage(qr, qr_x_coord, qr_y_coord, width=qr_size, height=qr_size)
    # BBOX: qr
    boxes["qr"] = (qr_x_coord, qr_y_coord, qr_x_coord + qr_size, qr_y_coord + qr_size)
    y -= 110

    c.setFont("Courier", 7)
    c.drawCentredString(x0 + ticket_w / 2, y, "Comprobante No Fiscal - Ley 27.430")
    y -= 8
    c.drawCentredString(x0 + ticket_w / 2, y, "Controlado por AFIP - RG 1415/03")
    y -= 8
    c.drawCentredString(x0 + ticket_w / 2, y, "Gracias por su compra")
    c.save()

    # --- Generar líneas YOLO ---
    yolo_lines = []
    for key, box in boxes.items():
        cls_id = YOLO_CLASS_MAP.get(key, None)
        if cls_id is None:
            continue
        cx, cy, w, h = bbox_to_yolo(box, WIDTH_PT, HEIGHT_PT)
        yolo_lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

    return yolo_lines


# -------------------- Generador --------------------
# ... (funciones gen_ticket_meta y gen_factura_meta se mantienen igual)
def gen_ticket_meta():
    emisor = {"cuit": gen_cuit()}
    items = gen_items(random.randint(3, 8))
    meta = {
        "comercio": random.choice(["Supermercado Los Andes", "Kiosco 24hs", "Farmacia San José", "Panadería La Nueva"]),
        "direccion": fake.street_address() + ", " + fake.city(),
        "emisor": emisor,
        "nro": random.randint(1000, 9999),
        "fecha": fake.date_time_this_year().strftime("%d/%m/%Y %H:%M"),
        "items": items,
        "pago": random.choice(["Efectivo", "Tarjeta Débito", "Tarjeta Crédito", "Mercado Pago"]),
        "qr": f"https://qr.afip.gob.ar/?t={random.randint(100000, 999999)}"
    }
    return meta


def gen_factura_meta(tipo):
    emisor = {
        "razon_social": fake.company() + " " + random.choice(["S.A.", "SRL", "S.R.L."]),
        "cuit": gen_cuit(),
        "iva": "Responsable Inscripto" if tipo in ["A", "B"] else "Monotributista",
        "domicilio": fake.street_address() + ", " + fake.city()
    }

    if tipo == "A":
        receptor = {"nombre": fake.company(), "cuit": gen_cuit(), "iva": "Responsable Inscripto"}
    elif tipo == "B":
        receptor = {"nombre": random.choice([fake.name(), "Consumidor Final"]), "cuit": "",
                    "iva": random.choice(["Consumidor Final", "Monotributista", "Exento"])}
    else:
        receptor = {"nombre": fake.name(), "cuit": "", "iva": random.choice(["Consumidor Final", "Exento"])}

    items = gen_items(random.randint(2, 6))
    fecha = fake.date_between("-720d", "today").strftime("%d/%m/%Y")
    meta = {
        "emisor": emisor,
        "receptor": receptor,
        "punto_venta": gen_pv(),
        "nro": gen_comp_num(),
        "fecha": fecha,
        "items": items,
        "CAE": gen_cae(),
        "CAE_vto": (datetime.date.today() + datetime.timedelta(days=7)).strftime("%d/%m/%Y"),
        "qr": f"https://qr.afip.gob.ar/?p={random.randint(100000000000, 999999999999)}",
        "cond_venta": random.choice(["Contado", "Tarjeta Débito", "Tarjeta Crédito", "Cuenta Corriente"])
    }
    return meta


def generate_dataset(n_each=10):
    annotations = {}

    # Facturas A, B, C
    for t in ["A", "B", "C"]:
        for i in range(n_each):
            meta = gen_factura_meta(t)
            fname_base = f"factura_{t}_{i + 1:04d}"
            pdf_path = os.path.join(TIPOS[t], fname_base + ".pdf")
            txt_path = os.path.join(TIPOS[t], fname_base + ".txt")

            yolo_lines = draw_factura(pdf_path, t, meta)

            # Guardar el archivo de anotación YOLO
            with open(txt_path, "w", encoding="utf-8") as f:
                for line in yolo_lines:
                    f.write(line + "\n")

            annotations[f"{t}/{fname_base}.pdf"] = meta

    # Tickets
    for i in range(n_each):
        meta = gen_ticket_meta()
        fname_base = f"ticket_{i + 1:04d}"
        pdf_path = os.path.join(TIPOS["TICKET"], fname_base + ".pdf")
        txt_path = os.path.join(TIPOS["TICKET"], fname_base + ".txt")

        yolo_lines = draw_ticket(pdf_path, meta)

        # Guardar el archivo de anotación YOLO
        with open(txt_path, "w", encoding="utf-8") as f:
            for line in yolo_lines:
                f.write(line + "\n")

        annotations[f"ticket/{fname_base}.pdf"] = meta

    with open(ANNOT_FILE, "w", encoding="utf-8") as f:
        json.dump(annotations, f, indent=2, ensure_ascii=False)

    print("✅ Dataset generado en PDF + .txt YOLO en:", os.path.abspath(OUTDIR))


if __name__ == "__main__":
    generate_dataset(n_each=2000)