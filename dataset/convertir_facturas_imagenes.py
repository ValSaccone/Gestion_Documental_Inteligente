import os
import mimetypes
from pdf2image import convert_from_path
import cv2


def convert_to_image(input_path, output_path):
    mime, _ = mimetypes.guess_type(input_path)

    # Si el archivo es PDF
    if mime == "application/pdf":
        pages = convert_from_path(input_path, dpi=300)
        img = pages[0]  # primera página
        img.save(output_path, "PNG")
        return output_path

    # Si ya es imagen
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
    Recorre todas las carpetas y convierte cada PDF en PNG.
    Los archivos de imagen y txt se guardan en out_root.
    """

    print(f"Leyendo dataset desde: {root}")

    os.makedirs(out_root, exist_ok=True)

    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)

        if not os.path.isdir(folder_path):
            continue

        # Recorrer PDFs dentro de cada carpeta
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(folder_path, filename)

            name_without_ext = filename.replace('.pdf', '')

            if name_without_ext.lower().startswith(folder.lower()):
                base_name = name_without_ext
            else:
                base_name = f"{folder}_{name_without_ext}"

            out_name = f"{base_name}.png"

            out_path = os.path.join(out_root, out_name)

            print(f"Convirtiendo: {pdf_path}")
            convert_to_image(pdf_path, out_path)

            txt_name = filename.replace(".pdf", ".txt")
            txt_path_origen = os.path.join(folder_path, txt_name)

            if os.path.exists(txt_path_origen):
                txt_path_destino = os.path.join(out_root, f"{base_name}.txt")
                os.rename(txt_path_origen, txt_path_destino)

    print("Conversión completada.")


def mover_anotaciones_txt(
        root="facturas",
        out_root="dataset_imagenes"
):


    print("\nIniciando movimiento de archivos de anotación (.txt)...")

    os.makedirs(out_root, exist_ok=True)

    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)

        if not os.path.isdir(folder_path):
            continue

        for filename in os.listdir(folder_path):

            if not filename.lower().endswith(".pdf"):
                continue

            name_without_ext = filename.replace('.pdf', '')

            if name_without_ext.lower().startswith(folder.lower()):
                base_name = name_without_ext
            else:
                base_name = f"{folder}_{name_without_ext}"


            txt_name = filename.replace(".pdf", ".txt")
            txt_path_origen = os.path.join(folder_path, txt_name)

            if os.path.exists(txt_path_origen):
                txt_path_destino = os.path.join(out_root, f"{base_name}.txt")


                os.rename(txt_path_origen, txt_path_destino)
                print(f"TXT Movido: {txt_path_origen} -> {txt_path_destino}")

    print("Movimiento de anotaciones completado.")


if __name__ == "__main__":
    process_dataset()
    mover_anotaciones_txt()