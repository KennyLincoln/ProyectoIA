import time
from typing import Callable, Any

from src.consumir_gemini import armar_peticion, extraer_texto, enviar_peticion

def con_reintento(
    funcion: Callable[[], Any],
    intentos: int = 3,
    espera_segundos: int = 2,
) -> Any:
    for intento in range(intentos):
        try:
            return funcion()
        except Exception as e:
            if intento == intentos - 1:
                raise
            print(f"Intento {intento + 1} de {intentos} falló ({e}). Reintentando...")
            time.sleep(espera_segundos)

    #Cómo ejecuto esto?
MODELO = "gemini-3.6-flash"
PREGUNTA = "Hola, ¿cómo estás?"
SYSTEM_INSTRUCTION = "Eres un asistente amigable y respondes en máximo 2 palabras."


def main():
    url, body = armar_peticion(MODELO, PREGUNTA, SYSTEM_INSTRUCTION)

    try:
        datos = con_reintento(lambda: enviar_peticion(url, body))
        print(extraer_texto(datos))
    except Exception as error:
        print("No se pudo completar la operación:", error)


if __name__ == "__main__":
    main()