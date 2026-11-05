from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI #Modelo
from langchain_core.prompts import PromptTemplate #Plantilla -> Prompt dinámico
from langchain_core.output_parsers import StrOutputParser #Parsea la respuesta a texto
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough, RunnableLambda)

import logging #Generar un archivo de log con los errores

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="error.log",
    filemode="a",
    encoding="utf-8",
    force=True
)
logger = logging.getLogger(__name__)

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra: "
    "pregunta, queja o sugerencia. Responde solo con esa palabra. \n\n {mensaje}"
)


def construir_paso_clasificacion(modelo):
    return (
        plantilla_clasificacion
        | modelo
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )


paso_clasificacion = construir_paso_clasificacion(modelo)

cadena_pregunta = (
    PromptTemplate.from_template("Responde esta pregunta técnica con precisión: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_queja = (
    PromptTemplate.from_template("Responde esta queja con empatía, reconociendo el problema antes de ofrecer una solución: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template("Agradece esta sugerencia y explica cómo se evaluará dentro del producto: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)


#Fallback: respuesta de respaldo ante caídas del LLM
def fallback_con_log(x):
    logger.warning("Cadena principal falló. Activando respuesta genérica, Error: %s", x.get("error"))
    return "Gracias por tu mensaje. Un miembro de nuestro equipo te va a responder pronto."


respuesta_generica = RunnableLambda(fallback_con_log)


def construir_cadena_queja_segura(cadena_queja):
    return cadena_queja.with_fallbacks([respuesta_generica], exception_key="error")


def construir_cadena_con_enrutamiento(
    paso_clasificacion,
    cadena_queja=None,
    cadena_sugerencia=None,
    cadena_pregunta=None,
):
    cadena_queja = cadena_queja or RunnablePassthrough()
    cadena_sugerencia = cadena_sugerencia or RunnablePassthrough()
    cadena_pregunta = cadena_pregunta or RunnablePassthrough()
    bifurcacion = RunnableBranch(
        (lambda x: x["categoria"] == "queja", cadena_queja),
        (lambda x: x["categoria"] == "sugerencia", cadena_sugerencia),
        cadena_pregunta,
    )
    return RunnablePassthrough.assign(categoria=paso_clasificacion) | bifurcacion


cadena_con_enrutamiento = construir_cadena_con_enrutamiento(
    paso_clasificacion=paso_clasificacion,
    cadena_queja=construir_cadena_queja_segura(cadena_queja),
    cadena_sugerencia=cadena_sugerencia,
    cadena_pregunta=cadena_pregunta,
)


def procesar_mensaje_seguro(cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        logger.error("Error procesando mensaje: %s", error)
        return "No pudimos procesar tu mensaje en este momento. Intenta de nuevo más tarde."


if __name__ == "__main__":
    mensaje = "Llevo varios días sin poder entrar a mi cuenta."
    print(procesar_mensaje_seguro(cadena_con_enrutamiento, mensaje))

# Entrada inicial: {"mensaje": "Deberían de tener más agentes disponibles."}
#                   │
#                   ▼
# RunnablePassthrough
#   1: Pasa el mensaje a paso_clasificacion -> Return "sugerencia"
#   2: Fusiono clasificacion y mensaje
#   3: Return {"mensaje": "Deberían de tener más agentes disponibles.", "clasificacion": "sugerencia"}
#                   │
#                   ▼
# bifurcacion (RunnableBranch)
#   ¿clasificacion == "queja"? NO
#   ¿clasificacion == "sugerencia" SI
#       Entra a la cadena_sugerencia
#       cadena_sugerencia.invoke({"mensaje": "Deberían de tener más agentes disponibles.", "clasificacion": "sugerencia"})
#       Return respuesta final generada