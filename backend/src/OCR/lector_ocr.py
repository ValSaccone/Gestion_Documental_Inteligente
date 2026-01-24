import pytesseract
import cv2

def limpiar_texto(txt):
    if not txt:
        return ""
    return " ".join(txt.replace("\n", " ").split())

def ocr_roi(img):
    if img is None:
        return "UNREADABLE"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    config = "--oem 3 --psm 6 -l eng"

    try:
        texto = pytesseract.image_to_string(thresh, config=config)
        texto = limpiar_texto(texto)
        return texto if texto else ""
    except:
        return ""
