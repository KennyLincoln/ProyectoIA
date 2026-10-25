import consumir_gemini
import time
import statistics

def evaluar_modelo(nombre_modelo, pregunta, precio_entrada, precio_salida, repeticiones=4):
    print("=" * 70)
    print(f" EVALUANDO MODELO: {nombre_modelo}")
    print("=" * 70)

    latencias = []
    costos = []

    for i in range(1, repeticiones + 1):
        print(f"\n--- Intento {i} de {repeticiones} ({nombre_modelo}) ---")
        try:
            url, body = consumir_gemini.armar_peticion(
                modelo=nombre_modelo,
                pregunta=pregunta,
                system_instruction="Eres un asistente amigable y respondes en máximo 2 frases."
            )

            inicio = time.perf_counter()
            datos = consumir_gemini.enviar_peticion(url, body)
            latencia = time.perf_counter() - inicio

            costo = consumir_gemini.calcular_costo(datos, precio_entrada, precio_salida)
            respuesta = consumir_gemini.extraer_texto(datos)
        except Exception as e:
            print(f"Error: {e}")
            continue

        latencias.append(latencia)
        costos.append(costo)
        print(f"Latencia:  {latencia:.2f} segundos")
        print(f"Costo:     ${costo:.6f} USD")
        print(f"Respuesta: {respuesta}")

    print("\n" + "-" * 40)
    print(f" RESUMEN {nombre_modelo}:")
    if latencias:
        print(f" Latencia promedio: {statistics.mean(latencias):.2f} segundos")
        print(f" Costo promedio:    ${statistics.mean(costos):.6f} USD")
    else:
        print(" Todos los intentos fallaron.")
    print("-" * 40 + "\n")


pregunta_prueba = "¿Cual es la latencia"

modelos = [
    {
        "nombre": "gemini-3.6-flash",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375,
    },
    {
        "nombre": "gemini-3.5-flash-lite",
        "precio_entrada": 0.00000030,
        "precio_salida": 0.00000250,
    },
]

if __name__ == "__main__":
    for config in modelos:
        evaluar_modelo(
            nombre_modelo=config["nombre"],
            pregunta=pregunta_prueba,
            precio_entrada=config["precio_entrada"],
            precio_salida=config["precio_salida"],
        )