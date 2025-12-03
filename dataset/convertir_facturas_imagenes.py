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
    y convierte cada PDF en PNG. Los archivos de imagen y TXT
    se guardan en una única carpeta plana (out_root).
    """

    print(f"Leyendo dataset desde: {root}")

    # Aseguramos que la carpeta de salida (plana) exista
    os.makedirs(out_root, exist_ok=True)

    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)

        if not os.path.isdir(folder_path):
            continue  # saltar archivos como annotations.json

        # Recorrer PDFs dentro de cada carpeta
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(folder_path, filename)

            # 💡 CORRECCIÓN CLAVE:
            # 1. Eliminar '.pdf'
            name_without_ext = filename.replace('.pdf', '')

            # 2. Verificar si el nombre del archivo ya contiene el nombre de la carpeta
            if name_without_ext.lower().startswith(folder.lower()):
                # Si es así, usamos solo el nombre del archivo (ya es único y correcto)
                base_name = name_without_ext
            else:
                # Si no, concatenamos el nombre de la carpeta para asegurar unicidad
                base_name = f"{folder}_{name_without_ext}"
            # --- FIN CORRECCIÓN CLAVE ---

            out_name = f"{base_name}.png"

            # La ruta de salida apunta directamente a la carpeta raíz 'out_root'
            out_path = os.path.join(out_root, out_name)

            print(f"Convirtiendo: {pdf_path}")
            convert_to_image(pdf_path, out_path)

            # Mover y Renombrar el archivo TXT de Anotación
            txt_name = filename.replace(".pdf", ".txt")
            txt_path_origen = os.path.join(folder_path, txt_name)

            if os.path.exists(txt_path_origen):
                # Usamos el base_name corregido para el destino del TXT
                txt_path_destino = os.path.join(out_root, f"{base_name}.txt")
                os.rename(txt_path_origen, txt_path_destino)

    print("Conversión completada.")


def mover_anotaciones_txt(
        root="facturas",
        out_root="dataset_imagenes"
):
    """
    Busca los archivos .txt de anotación en las subcarpetas de 'root'
    y los MUEVE a la carpeta plana 'out_root', renombrándolos.
    """

    print("\nIniciando movimiento de archivos de anotación (.txt)...")

    # Aseguramos que la carpeta de destino de los TXT exista (ya debería existir)
    os.makedirs(out_root, exist_ok=True)

    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)

        if not os.path.isdir(folder_path):
            continue

            # Recorremos los archivos en busca de los PDF para obtener el 'base_name'
        for filename in os.listdir(folder_path):

            # Solo buscamos PDFs para saber cómo se llama el TXT
            if not filename.lower().endswith(".pdf"):
                continue

            # --- Lógica de Movimiento del TXT ---

            name_without_ext = filename.replace('.pdf', '')

            if name_without_ext.lower().startswith(folder.lower()):
                base_name = name_without_ext
            else:
                base_name = f"{folder}_{name_without_ext}"


            txt_name = filename.replace(".pdf", ".txt")
            txt_path_origen = os.path.join(folder_path, txt_name)

            if os.path.exists(txt_path_origen):
                txt_path_destino = os.path.join(out_root, f"{base_name}.txt")

                # Mueve el TXT de su origen a la carpeta plana y lo renombra
                os.rename(txt_path_origen, txt_path_destino)
                print(f"TXT Movido: {txt_path_origen} -> {txt_path_destino}")

    print("Movimiento de anotaciones completado.")


if __name__ == "__main__":
    process_dataset()
    mover_anotaciones_txt()