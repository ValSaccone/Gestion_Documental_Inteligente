from enum import Enum
from fastapi import status, HTTPException
import logging

logger = logging.getLogger(__name__)

ERROR_RESPONSES = {
    "datos_invalidos": {
        "message": "Los datos ingresados son inválidos.",
        "status": status.HTTP_400_BAD_REQUEST,
        "error": "Bad Request"
    },
    "no_encontrado": {
        "message": "No se encontró el recurso solicitado.",
        "status": status.HTTP_404_NOT_FOUND,
        "error": "Not Found"
    },
    "datos_duplicados": {
        "message": "Los datos ingresados ya existen.",
        "status": status.HTTP_409_CONFLICT,
        "error": "Conflict"
    },
    "error_interno": {
        "message": "Error interno del servidor.",
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "error": "Internal Server Error"
    },
    "imagen_invalida": {
        "message": "El archivo subido no es una imagen válida.",
        "status": status.HTTP_400_BAD_REQUEST,
        "error": "Bad Request"
    },
    "pdf_invalido": {
        "message": "El PDF no pudo ser procesado.",
        "status": status.HTTP_400_BAD_REQUEST,
        "error": "Bad Request"
    },
}

class ResponseErrors(str, Enum):
    DATOS_INVALIDOS = "datos_invalidos"
    NO_ENCONTRADO = "no_encontrado"
    DATOS_DUPLICADOS = "datos_duplicados"
    ERROR_INTERNO = "error_interno"
    IMAGEN_INVALIDA = "imagen_invalida"
    PDF_INVALIDO = "pdf_invalido"


class ServiceError(Exception):
    def __init__(self, error_key: ResponseErrors, detail: str | None = None):
        self.error_key = error_key
        self.detail = detail


def raise_service_error(error_key: ResponseErrors, detail: str | None = None):
    error = ERROR_RESPONSES[error_key.value]

    if detail:
        logger.error(f"{error_key.value}: {detail}")
        message = detail
    else:
        message = error["message"]

    raise HTTPException(
        status_code=error["status"],
        detail={
            "error": error["error"],
            "message": message
        }
    )
