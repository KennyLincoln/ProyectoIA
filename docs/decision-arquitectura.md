# Decisión de arquitectura: elección del modelo

Fecha de la comparación: Miercoles 21 de Octubre del 2026
Nombre de la miniaplicación: "WIL"

## Modelo elegido

Elegí el modelo: **gemini-3.6-flash**

Mi miniaplicación sirve para: Detectar el mejor modelo de IA según criterios determinados.

Los requisitos que necesito cumplir son:

* Respuestas rápidas, porque el usuario espera la respuesta en pantalla.
* Disponibilidad estable, sin fallos frecuentes del servicio.
* Costo bajo por petición.

## Diagrama de arquitectura

![Diagrama de arquitectura](./diagrama_arquitectura.png)

## Comparación de candidatos

- Estas son las preguntas y condiciones con las cuales se midieron ambos modelos:

* Preguntas y/o condiciones:

1. Pregunta enviada 4 veces a cada modelo: "¿Cual es la latencia".
2. Misma instrucción de sistema en ambos: "Eres un asistente amigable y respondes en máximo 2 frases."
3. Misma sesión de pruebas y mismas condiciones de red (21-10-2026).

| Criterio | gemini-3.6-flash | gemini-3.1-flash-lite |
|---|---|---|
| Tarifa de entrada en USD por millón de tokens | $0.10 | $0.75 |
| Tarifa de salida en USD por millón de tokens | $0.30 | $3.75 |
| Latencias observadas en segundos | 4.66, 4.47, 4.91, 4.61 | 23.27, 11.28 (2 intentos fallaron con error 503) |
| Latencia promedio en segundos | 4.66 | 17.28 |
| Costo promedio por petición (USD) | $0.000121 | $0.000119 |
| Peticiones exitosas | 4 de 4 | 2 de 4 |
| Calidad para nuestra miniaplicación | Buena: respuestas claras y coherentes, distintas entre intentos | Buena: respuesta coherente, pero idéntica en los dos intentos exitosos |

Fuente de las tarifas:
  
## Justificación

Elegí gemini-3.6-flash porque para mi aplicación la rapidez de respuesta y la estabilidad importan más que el costo.
Lo que observé en las pruebas fue que el costo por petición fue casi idéntico ($0.000121 frente a $0.000119), pero gemini-3.6-flash respondió en promedio en 4.66 segundos contra 17.28 segundos, y completó las 4 peticiones sin errores.
El criterio más relevante para mi decisión fue la latencia, junto con la disponibilidad, ya que el costo no marcó diferencia.
Una limitación que encontré en mi elección fue que 4.66 segundos sigue siendo una espera notable para el usuario, y que la muestra fue pequeña y de una sola sesión, así que los resultados podrían variar en otro momento.

## Alternativa descartada y por qué

Descarté gemini-3.1-flash-lite porque, aunque su costo por petición fue igual de bajo, su latencia promedio fue unas 3.7 veces mayor (17.28 s) y falló en 2 de 4 peticiones con error 503 durante mi medición. Para una miniaplicación donde el usuario espera una respuesta ágil, esa lentitud e inconsistencia no se justifican.