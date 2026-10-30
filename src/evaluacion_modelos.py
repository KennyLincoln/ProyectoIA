import consumir_gemini
import time
import statistics

def evaluar_modelo(nombre_modelo, pregunta, precio_entrada, precio_salida, repeticiones=4):
    """
    Ejecuta 'repeticiones' veces la misma petición para un modelo específico.
    Calcula e imprime Latencia, Costo y Respuesta de cada intento,
    además del promedio de latencia al final.
    """    
    print("=" * 70)
    print(f" EVALUANDO MODELO: {nombre_modelo}")
    print("=" * 70)

    latencias = []
    costos = []

    for i in range(1, repeticiones + 1):
        print(f"\n--- Intento {i} de {repeticiones} ({nombre_modelo}) ---")
        try: 
            # 1. Armar petición (puedes pasar el modelo si tu función lo requiere)
            url, body = consumir_gemini.armar_peticion(
                modelo=nombre_modelo, 
                pregunta=pregunta,
                system_instruction="Eres un asistente amigable y respondes en máximo 2 frases."
            )
            # 2. Medir latencia
            inicio = time.perf_counter()
            datos = consumir_gemini.enviar_peticion(url, body)
            latencia = time.perf_counter() - inicio

           # 3. Calcular costo
            costo = consumir_gemini.calcular_costo(datos, precio_entrada, precio_salida)
            # 4. Extraer respuesta
            respuesta = consumir_gemini.extraer_texto(datos)
        except Exception as e:
            print(f"Error: {e}")
            continue

        latencias.append(latencia)
        costos.append(costo)
        # 5. Imprimir resultados de la petición actual
        print(f"Latencia:  {latencia:.2f} segundos")
        print(f"Costo:     ${costo:.6f} USD")
        print(f"Respuesta: {respuesta}")

        # Resumen acumulado del modelo
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

# Procesar los 3 modelos consecutivamente
if __name__ == "__main__":
    for config in modelos:
        evaluar_modelo(
            nombre_modelo=config["nombre"],
            pregunta=pregunta_prueba,
            precio_entrada=config["precio_entrada"],
            precio_salida=config["precio_salida"],
        )