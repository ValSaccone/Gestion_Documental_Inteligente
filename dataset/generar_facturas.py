import os, json, random
from faker import Faker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import qrcode
from io import BytesIO

fake = Faker("es_AR")

# CONFIGURACION
OUTDIR = "facturas"
os.makedirs(OUTDIR, exist_ok=True)

TIPOS = {"A": "001", "B": "006", "C": "011"}

WIDTH, HEIGHT = A4
M = 10 * mm

YOLO_CLASS_MAP = {
    "tipo_factura": 0,
    "razon_social": 1,
    "cuit_emisor": 2,
    "numero_factura": 3,
    "fecha": 4,
    "tabla_items": 5,
    "total": 6
}

# HELPERS

def gen_cuit():
    return f"{random.choice([20,23,27,30])}-{random.randint(10000000,99999999)}-{random.randint(0,9)}"

def money(v):
    return f"$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def make_qr(data):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return ImageReader(bio)

def bbox_to_yolo(box):
    x1, y1, x2, y2 = box
    y1i = HEIGHT - y2
    y2i = HEIGHT - y1
    return (
        ((x1+x2)/2)/WIDTH,
        ((y1i+y2i)/2)/HEIGHT,
        (x2-x1)/WIDTH,
        (y2i-y1i)/HEIGHT
    )

# DATOS
def gen_items():
    items=[]
    for _ in range(random.randint(1,3)):
        q=random.randint(1,3)
        u=round(random.uniform(500,3000),2)
        items.append({
            "desc": random.choice(["SERVICIO MENSUAL","QUINCENA","HONORARIOS"]),
            "cant": q,
            "sub": round(q*u,2)
        })
    return items

def gen_meta(tipo):

    if tipo == "A":
        iva_emisor = "Responsable Inscripto"
        iva_receptor = "IVA Responsable Inscripto"
    elif tipo == "B":
        iva_emisor = "Responsable Inscripto"
        iva_receptor = "Consumidor Final"
    else:  # C
        iva_emisor = "Monotributo"
        iva_receptor = "Consumidor Final"

    return {
        "emisor":{
            "razon": fake.company().upper(),
            "dom": fake.street_address()+" - Ciudad de Buenos Aires",
            "iva": iva_emisor,
            "cuit": gen_cuit(),
            "iibb": "123-456789-0",
            "inicio": "01/01/2018"
        },
        "receptor":{
            "razon": fake.company(),
            "cuit": gen_cuit(),
            "iva": iva_receptor,
            "dom": fake.street_address()+" - Capital Federal",
            "venta": "Cuenta Corriente"
        },
        "pv": f"{random.randint(1,9999):05d}",
        "nro": f"{random.randint(1,99999999):08d}",
        "fecha": fake.date_this_year().strftime("%d/%m/%Y"),
        "desde": "01/03/2025",
        "hasta": "31/03/2025",
        "vto": fake.date_this_year().strftime("%d/%m/%Y"),
        "items": gen_items(),
        "qr": "https://www.afip.gob.ar"
    }

# DIBUJAR FACTURA

def draw_factura(path, tipo, m):
    c = canvas.Canvas(path, pagesize=A4)
    boxes = {}

    c.rect(M, M, WIDTH-2*M, HEIGHT-2*M)

    # ORIGINAL
    c.rect(WIDTH/2-30*mm, HEIGHT-18*mm, 60*mm, 8*mm)
    c.setFont("Helvetica-Bold",9)
    c.drawCentredString(WIDTH/2, HEIGHT-15*mm, "ORIGINAL")

    # BLOQUE SUPERIOR
    top_y = HEIGHT-75*mm
    c.rect(M+5, top_y, WIDTH-2*M-10, 55*mm)

    # TIPO FACTURA
    bx = WIDTH / 2 - 12 * mm
    by = top_y + 36 * mm
    boxes["tipo_factura"] = (bx, by + 2 * mm, bx + 24 * mm, by + 12 * mm)
    c.rect(bx, by, 24 * mm, 18 * mm)
    # letra centrada en el nuevo box
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(WIDTH / 2, by + 8 * mm, tipo)
    c.setFont("Helvetica", 7)
    c.drawCentredString(WIDTH / 2, by + 2 * mm, f"COD. {TIPOS[tipo]}")

    # IZQUIERDA EMISOR
    c.setFont("Helvetica",8)
    lx = M + 10
    ly = by - 4*mm

    c.drawString(lx, ly+6*mm, "Razón Social:")
    c.drawString(lx, ly, "Domicilio Comercial:")
    c.drawString(lx, ly-6*mm, "Condición frente al IVA:")

    c.setFont("Helvetica-Bold",8)
    c.drawString(lx+35*mm, ly+6*mm, m["emisor"]["razon"])
    c.setFont("Helvetica",8)
    c.drawString(lx+35*mm, ly, m["emisor"]["dom"])
    c.drawString(lx+35*mm, ly-6*mm, m["emisor"]["iva"])

    # razón social (YOLO)
    boxes["razon_social"] = (
        lx+35*mm,
        ly+4*mm,
        lx+95*mm,
        ly+12*mm
    )

    # DERECHA FACTURA
    c.setFont("Helvetica-Bold",11)
    c.drawRightString(WIDTH-M-10, ly+6*mm, m["emisor"]["razon"])

    c.setFont("Helvetica",8)
    c.drawRightString(
        WIDTH-M-10,
        ly,
        f"Punto de Venta {m['pv']}  Comp. Nro {m['nro']}"
    )
    c.drawRightString(
        WIDTH-M-10,
        ly-6*mm,
        f"Fecha de Emisión: {m['fecha']}"
    )
    c.drawRightString(
        WIDTH-M-10,
        ly-12*mm,
        f"CUIT: {m['emisor']['cuit']}"
    )

    # número factura
    boxes["numero_factura"] = (
        WIDTH-M-60,
        ly-1*mm,
        WIDTH-M-10,
        ly+4*mm
    )

    # fecha emisión
    boxes["fecha"] = (
        WIDTH-M-60,
        ly-7*mm,
        WIDTH-M-10,
        ly-3*mm
    )

    # CUIT emisor
    boxes["cuit_emisor"] = (
        WIDTH-M-60,
        ly-13*mm,
        WIDTH-M-10,
        ly-9*mm
    )

    # PERÍODO FACTURADO
    py = top_y - 12*mm
    c.rect(M+5, py, WIDTH-2*M-10, 12*mm)
    c.setFont("Helvetica",8)
    c.drawString(
        M+10, py+4*mm,
        f"Período Facturado Desde: {m['desde']}  Hasta: {m['hasta']}   Fecha de Vto. para el pago: {m['vto']}"
    )

    # CLIENTE / RECEPTOR
    cy = py - 22*mm
    c.rect(M+5, cy, WIDTH-2*M-10, 22*mm)
    c.setFont("Helvetica",8)
    c.drawString(M+10, cy+14*mm, f"CUIT: {m['receptor']['cuit']}")
    c.drawString(M+10, cy+8*mm, f"Apellido y Nombre / Razón Social: {m['receptor']['razon']}")
    c.drawString(M+10, cy+2*mm, f"Condición frente al IVA: {m['receptor']['iva']}")
    c.drawRightString(WIDTH-M-10, cy+14*mm, f"Fac. {tipo}: {m['pv']}-{m['nro']}")
    c.drawRightString(WIDTH-M-10, cy+8*mm, f"Domicilio: {m['receptor']['dom']}")
    c.drawRightString(WIDTH-M-10, cy+2*mm, f"Condición de Venta: {m['receptor']['venta']}")

    # TABLA ITEMS
    ty = cy - 45*mm
    c.rect(M+5, ty, WIDTH-2*M-10, 40*mm)

    c.setFont("Helvetica-Bold",8)
    c.drawString(M+10, ty+34*mm, "Producto / Servicio")
    c.drawRightString(WIDTH-M-80, ty+34*mm, "Cantidad")
    c.drawRightString(WIDTH-M-30, ty+34*mm, "Subtotal")

    yy = ty+26*mm
    total = 0
    c.setFont("Helvetica",8)

    for it in m["items"]:
        c.drawString(M+10, yy, it["desc"])
        c.drawRightString(WIDTH-M-80, yy, str(it["cant"]))
        c.drawRightString(WIDTH-M-30, yy, money(it["sub"]))
        total += it["sub"]
        yy -= 7*mm

    boxes["tabla_items"] = (
        M + 5,
        ty + 10 * mm,
        WIDTH - M - 5,
        ty + 40 * mm
    )

    # TOTAL
    c.setFont("Helvetica-Bold",9)
    c.drawRightString(
        WIDTH-M-10,
        ty-8*mm,
        f"Importe Total: {money(total)}"
    )

    boxes["total"] = (
        WIDTH-M-90,
        ty-12*mm,
        WIDTH-M-10,
        ty-6*mm
    )

    # QR
    qr = make_qr(m["qr"])
    c.drawImage(qr, M+10, M+10, 30*mm, 30*mm)

    c.save()

    # YOLO
    yolo = []
    for k, b in boxes.items():
        cx, cy, w, h = bbox_to_yolo(b)
        yolo.append(f"{YOLO_CLASS_MAP[k]} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

    return yolo

# GENERAR
def generate(n=100):
    ann={}
    for t in TIPOS:
        os.makedirs(f"{OUTDIR}/Factura_{t}", exist_ok=True)
        for i in range(n):
            meta=gen_meta(t)
            name=f"factura_{t}_{i:04d}"
            pdf=f"{OUTDIR}/Factura_{t}/{name}.pdf"
            txt=pdf.replace(".pdf",".txt")
            yolo=draw_factura(pdf,t,meta)
            with open(txt,"w") as f:
                f.write("\n".join(yolo))
            ann[f"{t}/{name}.pdf"]=meta

    with open(os.path.join(OUTDIR,"annotations.json"),"w",encoding="utf8") as f:
        json.dump(ann,f,indent=2,ensure_ascii=False)

    print("Facturas A/B/C estilo ARCA generadas correctamente")

if __name__=="__main__":
    generate(2000)





