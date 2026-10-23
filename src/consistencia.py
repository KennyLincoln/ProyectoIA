import json
import time
from prompts.banco import BANCO_DE_PROMPT
from consumir_gemini import armar_peticion, enviar_peticion, extraer_texto, parsear_respuestas_json

INTENTOS = 3
registro = {}

try:
    for prompt in BANCO_DE_PROMPT:
        exitos = 0
        for intento in range(INTENTOS):
            url, body = armar_peticion(
                "gemini-3.5-flash-lite",
                prompt["ejemplo_usuario"],
                prompt["system_instruction"],
                prompt["response_schema"],
            )
            texto = extraer_texto(enviar_peticion(url, body))
            try:
                parsear_respuestas_json(texto, prompt["claves_esperadas"])
                exitos += 1
            except ValueError as error:
                print(f"intento {intento + 1} falló: {error}")
            time.sleep(1)

        print(f"{prompt['nombre']}: {exitos}/{INTENTOS} respuestas válidas")
        registro[prompt["nombre"]] = {"exitos": exitos, "intentos": INTENTOS}

    with open("src/prompts/registro_resultados.json", "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, indent=2, ensure_ascii=False)

except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación:", error)