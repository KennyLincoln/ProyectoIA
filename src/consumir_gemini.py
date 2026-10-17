import os
import requests
from dotenv import load_dotenv

load_dotenv()

#constantes
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

#función para crear la solicitud
def armar_peticion(pregunta): #pregunta = "Confirma la conexion"
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}" #url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
    body = {
        "contents": 
             [{"parts": [{"text": pregunta}]}]
          }
    return url, body

#armar_peticion_openai -> url, body

#función envía la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos momentos.")
    except requests.exceptions.Timeout:
        raise RuntimeError("Se agoto el tiempo. Intenta de nuevo en unos momentos.")

    if respuesta.status_code != 200:
        raise RuntimeError(f"Error en la petición. Status Code:{respuesta.status_code}")

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")

#función procesa y extrae dato
def extraer_texto(datos): #Gemini
    try:
       return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
       raise RuntimeError("La respuesta no recibe el texto generado en el lugar definido.")

def obtener_dato_de_prueba(pregunta): # pregunta = "confirma la conexion"
    url, body = armar_peticion(pregunta) #obtener url y body
    #url = resultado de armar_peticion
    #body = resultado de armar_peticion
    datos = enviar_peticion(url, body)
    return extraer_texto(datos)

try:
    print(obtener_dato_de_prueba("Hola, dime en una frace si es que la API esta funcionando"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación.", error)
