#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador sintético de facturas argentinas (A, B, C) y tickets comunes.
Produce PDFs en carpeta facturas_dataset/ y un annotations.json.
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
OUTDIR = "facturas_dataset"
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

# -------------------- Helpers --------------------

def gen_cuit():
    pref = random.choice([20,23,24,27,30,33,34])
    mid = random.randint(10000000,99999999)
    end = random.randint(0,9)
    return f"{pref:02d}-{mid:08d}-{end}"

def gen_cae(): return "".join(str(random.randint(0,9)) for _ in range(14))
def gen_pv(): return f"{random.randint(1,9999):04d}"
def gen_comp_num(): return f"{random.randint(1,99999999):08d}"
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
        q = random.randint(1,5)
        u = round(random.uniform(300, 15000),2)
        st = round(q*u,2)
        items.append({"cant": q, "desc": p, "unit": u, "subtotal": st})
    return items

def make_qr(data):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    bio = BytesIO(); img.save(bio, format="PNG"); bio.seek(0)
    return ImageReader(bio)

# -------------------- PDF DRAW --------------------

def draw_factura(path, tipo, meta):
    width, height = A4
    c = canvas.Canvas(path, pagesize=A4)
    m = 20*mm

    # Marco principal
    c.setStrokeColor(black)
    c.rect(m, m, width-2*m, height-2*m)

    # Recuadro con letra
    c.rect(width/2 - 10*mm, height - 35*mm, 20*mm, 20*mm)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 22*mm, tipo)

    # Encabezado empresa
    c.setFont("Helvetica-Bold", 14)
    c.drawString(m+5, height - 25*mm, meta["emisor"]["razon_social"])
    c.setFont("Helvetica", 9)
    c.drawString(m+5, height - 30*mm, f"CUIT: {meta['emisor']['cuit']}  |  IVA: {meta['emisor']['iva']}")
    c.drawString(m+5, height - 35*mm, f"Domicilio: {meta['emisor']['domicilio']}")

    # Info factura
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(width - m - 5, height - 25*mm, f"Factura {tipo}")
    c.setFont("Courier", 10)
    c.drawRightString(width - m - 5, height - 30*mm, f"P.V: {meta['punto_venta']} N° {meta['nro']}")
    c.setFont("Helvetica", 9)
    c.drawRightString(width - m - 5, height - 35*mm, f"Fecha: {meta['fecha']}")

    # Receptor
    c.line(m+5, height - 40*mm, width - m - 5, height - 40*mm)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(m+5, height - 46*mm, "Cliente:")
    c.setFont("Helvetica", 9)
    c.drawString(m+35, height - 46*mm, meta["receptor"]["nombre"])
    if meta["receptor"]["cuit"]:
        c.drawString(m+35, height - 51*mm, f"CUIT: {meta['receptor']['cuit']}")
    c.drawString(m+35, height - 56*mm, f"Condición frente al IVA: {meta['receptor']['iva']}")
    c.drawString(m+35, height - 61*mm, f"Condición de venta: {meta['cond_venta']}")

    # Tabla ítems
    start_y = height - 80*mm
    c.line(m+5, start_y, width - m - 5, start_y)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(m+8, start_y - 10, "Cant.")
    c.drawString(m+40, start_y - 10, "Descripción")
    c.drawRightString(width - m - 120, start_y - 10, "Precio Unit.")
    c.drawRightString(width - m - 40, start_y - 10, "Subtotal")
    c.line(m+5, start_y - 14, width - m - 5, start_y - 14)

    y = start_y - 28
    c.setFont("Helvetica", 9)
    for it in meta["items"]:
        c.drawString(m+8, y, str(it["cant"]))
        c.drawString(m+40, y, it["desc"])
        c.drawRightString(width - m - 120, y, format_money(it["unit"]))
        c.drawRightString(width - m - 40, y, format_money(it["subtotal"]))
        y -= 14

    # Totales
    base = sum(i["subtotal"] for i in meta["items"])
    if tipo == "A":
        iva = round(base * 0.21, 2)
        total = round(base + iva, 2)
        c.drawRightString(width - m - 120, y - 10, "Subtotal:")
        c.drawRightString(width - m - 40, y - 10, format_money(base))
        c.drawRightString(width - m - 120, y - 25, "IVA 21%:")
        c.drawRightString(width - m - 40, y - 25, format_money(iva))
    else:
        iva = 0
        total = base
        c.setFont("Helvetica-Oblique", 8)
        c.drawRightString(width - m - 40, y - 15, "IVA incluido en el precio final")

    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - m - 120, y - 45, "TOTAL:")
    c.drawRightString(width - m - 40, y - 45, format_money(total))

    # Pie
    cae, vto = meta["CAE"], meta["CAE_vto"]
    c.setFont("Helvetica", 8)
    c.drawString(m+5, 25*mm, f"CAE: {cae}  |  Vto CAE: {vto}")
    qr = make_qr(meta["qr"])
    c.drawImage(qr, width - m - 90, 15*mm, width=70, height=70)
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(width/2, 10*mm, "Documento generado sintéticamente — No válido fiscalmente")
    c.save()

# -------------------- Ticket Argentino Realista --------------------

def draw_ticket(path, meta):
    width, height = A4
    c = canvas.Canvas(path, pagesize=A4)
    ticket_w = 80 * mm
    x0 = (width - ticket_w) / 2
    y = height - 40 * mm

    c.setFont("Courier-Bold", 10)
    c.drawCentredString(x0 + ticket_w/2, y, meta["comercio"].upper())
    y -= 10
    c.setFont("Courier", 8)
    c.drawCentredString(x0 + ticket_w/2, y, f"CUIT: {meta['emisor']['cuit']} - IVA INSC.")
    y -= 10
    c.drawCentredString(x0 + ticket_w/2, y, meta["direccion"])
    y -= 10
    c.drawCentredString(x0 + ticket_w/2, y, f"Fecha: {meta['fecha']}  TICKET #{meta['nro']}")
    y -= 8
    c.line(x0, y, x0 + ticket_w, y)
    y -= 10

    for it in meta["items"]:
        desc = it["desc"][:20]
        c.drawString(x0 + 2 * mm, y, f"{it['cant']}x {desc}")
        c.drawRightString(x0 + ticket_w - 2 * mm, y, format_money(it["subtotal"]))
        y -= 8

    y -= 6
    c.line(x0, y, x0 + ticket_w, y)
    total = sum(i["subtotal"] for i in meta["items"])
    y -= 12
    c.setFont("Courier-Bold", 9)
    c.drawRightString(x0 + ticket_w - 2 * mm, y, f"TOTAL: {format_money(total)}")
    y -= 10
    c.setFont("Courier", 8)
    c.drawString(x0 + 2 * mm, y, f"Forma de pago: {meta['pago']}")
    y -= 30  # ⬅️ antes era 20, bajamos el QR más

    qr = make_qr(meta["qr"])
    c.drawImage(qr, x0 + ticket_w/2 - 25, y - 50, width=50, height=50)  # ⬅️ QR movido más abajo
    y -= 110

    c.setFont("Courier", 7)
    c.drawCentredString(x0 + ticket_w/2, y, "Comprobante No Fiscal - Ley 27.430")
    y -= 8
    c.drawCentredString(x0 + ticket_w/2, y, "Controlado por AFIP - RG 1415/03")
    y -= 8
    c.drawCentredString(x0 + ticket_w/2, y, "Gracias por su compra")
    c.save()

# -------------------- Generador --------------------

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
        "qr": f"https://qr.afip.gob.ar/?t={random.randint(100000,999999)}"
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
        receptor = {"nombre": random.choice([fake.name(), "Consumidor Final"]), "cuit": "", "iva": random.choice(["Consumidor Final", "Monotributista", "Exento"])}
    else:
        receptor = {"nombre": fake.name(), "cuit": "", "iva": random.choice(["Consumidor Final", "Exento"])}

    items = gen_items(random.randint(2,6))
    fecha = fake.date_between("-720d", "today").strftime("%d/%m/%Y")
    meta = {
        "emisor": emisor,
        "receptor": receptor,
        "punto_venta": gen_pv(),
        "nro": gen_comp_num(),
        "fecha": fecha,
        "items": items,
        "CAE": gen_cae(),
        "CAE_vto": (datetime.date.today()+datetime.timedelta(days=7)).strftime("%d/%m/%Y"),
        "qr": f"https://qr.afip.gob.ar/?p={random.randint(100000000000,999999999999)}",
        "cond_venta": random.choice(["Contado","Tarjeta Débito","Tarjeta Crédito","Cuenta Corriente"])
    }
    return meta

def generate_dataset(n_each=10):
    annotations = {}
    for t in ["A","B","C"]:
        for i in range(n_each):
            meta = gen_factura_meta(t)
            fname = f"factura_{t}_{i+1:04d}.pdf"
            path = os.path.join(TIPOS[t], fname)
            draw_factura(path, t, meta)
            annotations[f"{t}/{fname}"] = meta
    for i in range(n_each):
        meta = gen_ticket_meta()
        fname = f"ticket_{i+1:04d}.pdf"
        path = os.path.join(TIPOS["TICKET"], fname)
        draw_ticket(path, meta)
        annotations[f"ticket/{fname}"] = meta

    with open(ANNOT_FILE, "w", encoding="utf-8") as f:
        json.dump(annotations, f, indent=2, ensure_ascii=False)

    print("✅ Dataset generado en", os.path.abspath(OUTDIR))

if __name__ == "__main__":
    generate_dataset(n_each=3000)
