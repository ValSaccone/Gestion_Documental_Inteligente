import pytesseract
import cv2
import numpy as np

# En Linux podría no hacer falta especificar ruta
# En Windows tendrías algo como:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def limpiar_texto(txt):
    if txt is None:
        return ""
    return txt.replace("\n", " ").strip()

def ocr_roi(roi_path):
    """
    Aplica OCR a un ROI.
    Devuelve un texto limpio o 'UNREADABLE' si el OCR falla.
    """
    img = cv2.imread(roi_path)

    if img is None:
        return "UNREADABLE"

    # Preprocesamiento para OCR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    config = "--oem 3 --psm 6 -l spa"

    try:
        texto = pytesseract.image_to_string(thresh, config=config)
        texto = limpiar_texto(texto)

        return texto if texto != "" else "UNREADABLE"

    except Exception as e:
        print("Error OCR:", e)
        return "UNREADABLE"


if __name__ == "__main__":
    print(ocr_roi("./temp_rois/fecha.png"))
