# Límites de la métrica de evaluación

## Qué mide

Coincidencia de palabras (tokens, tras la limpieza de texto) entre la respuesta del modelo y una referencia corta, contando repeticiones: precisión, cobertura y F1. No mide significado.

## Modos de falla conocidos

- **Sinónimos y paráfrasis correctas puntúan casi cero.** Ejemplo: "¿Qué es un diccionario en Python?" obtuvo f1=0.0 con una respuesta correcta ("pares de clave-valor" frente a "relaciona claves con valores"), sin ninguna palabra en común.
- **Variantes de una misma palabra no cuentan como coincidencia.** Ejemplo: "¿Para qué sirve def?" obtuvo f1=0.133; la referencia dice "define una función" y la respuesta "definir funciones". Algo parecido pasó con try except (f1=0.235, "excepciones" frente a "errores").
- **Una respuesta correcta pero más larga que la referencia pierde precisión.** Ejemplo: "¿En qué año fue la primera publicación de Python?" obtuvo f1=0.636 con el año correcto (1991). En "¿Qué es Python?" la cobertura fue 1.0 y el f1 solo 0.667.
- **No existe un umbral que separe buenas de malas respuestas.** En mi muestra, las respuestas correctas van de f1=0.0 a 0.727; ni los 5 f1 más altos pasaron de 0.727.
- **La métrica no verifica detalles añadidos.** Ejemplo: en HTTP 403 la respuesta añade "por falta de permisos", una causa que la referencia no menciona; el f1 (0.261) no dice si ese detalle es correcto.
- **No observado en esta muestra:** datos incorrectos con f1 alto ni negaciones ausentes que inviertan el significado (los otros dos casos del Bloque 16). Con 10 casos revisados no puedo descartarlos, solo no aparecieron.

## Muestra revisada

10 casos de 20 respuestas generadas con `gemini-3.6-flash` (respuestas de una oración, máximo 15 palabras): los 5 con menor F1 y los 5 con mayor F1. Revisión realizada el 2026-11-07, con la rúbrica de tres preguntas (corrección factual, completitud, contradicción) y con apoyo de Claude, con el visto bueno de la profesora. Resultado: 9 casos correctos en lo esencial, 1 parcial (HTTP 403) y ninguna contradicción. Detalle en `docs/revision_manual.json`.

## Recomendación de uso

En este pipeline, F1 sirve para comparar promedios entre versiones del cliente en volumen, pero no para decidir si una respuesta individual es correcta: en mi muestra, F1 bajo y F1 alto resultaron igual de correctos. Revisar siempre a mano cualquier respuesta con fechas, cifras o nombres, y cualquier respuesta que añada detalles que la referencia no contiene.
