import os
import mimetypes
from pdf2image import convert_from_path
import cv2

def convert_to_image(input_path, output_path):
    mime, _ = mimetypes.guess_type(input_path)

    # --- Si el archivo es PDF ---
    if mime == "application/pdf":
        pages = convert_from_path(input_path, dpi=300)
        img = pages[0]  # primera página
        img.save(output_path, "PNG")
        return output_path

    # --- Si ya es imagen ---
    elif mime and mime.startswith("image"):
        img = cv2.imread(input_path)
        cv2.imwrite(output_path, img)
        return output_path

    else:
        raise ValueError(f"Formato no soportado: {input_path}")


def process_dataset(
    root="facturas",
    out_root="dataset_imagenes"
):
    """
    Recorre todas las carpetas (Factura_A, Factura_B, etc.)
    y convierte cada PDF en PNG manteniendo la estructura.
    """

    print(f"Leyendo dataset desde: {root}")

    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)

        if not os.path.isdir(folder_path):
            continue  # saltar archivos como annotations.json

        # Crear carpeta espejo en dataset/dataset_images/
        out_folder = os.path.join(out_root, folder)
        os.makedirs(out_folder, exist_ok=True)

        # Recorrer PDFs dentro de cada carpeta
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(folder_path, filename)
            out_name = filename.replace(".pdf", ".png")
            out_path = os.path.join(out_folder, out_name)

            print(f"Convirtiendo: {pdf_path}")
            convert_to_image(pdf_path, out_path)

    print("Conversión completada.")


if __name__ == "__main__":
    process_dataset()
