# Proyecto WIL — Especialización en Desarrollo con IA Generativa (Accenture)

WIL es una miniaplicación en Python orientada a WATERisLIFE, una ONG
que trabaja por el acceso a agua segura, saneamiento e higiene.

El objetivo es preparar un asistente que pueda orientar a personas
interesadas en donar, conocer el impacto de sus aportes y consultar
información de transparencia.

En esta primera etapa, el programa ejecuta preguntas de prueba desde
la terminal y utiliza la API de Gemini para obtener respuestas.
Una API permite que nuestro programa se comunique con un servicio externo.

## Qué hace el proyecto

El proyecto permite:

- Enviar preguntas a un modelo de inteligencia artificial.
- Recibir y procesar respuestas en formato JSON.
- Comprobar que las respuestas tengan la estructura esperada.
- Comparar modelos según su tiempo de respuesta y costo estimado.
- Mostrar mensajes cuando ocurre un error.

JSON es una forma de organizar información mediante nombres y valores.
Por ejemplo, una respuesta del asistente puede tener esta estructura:

```json
{
    "respuesta": "Puedes conocer las opciones para donar en el sitio de WATERisLIFE."
}
```

## Cómo empezar

Antes de comenzar, necesitas:

- **Python 3:** permite ejecutar el programa.
- **Git:** permite descargar el proyecto desde GitHub.
- **Visual Studio Code:** permite abrir y editar sus archivos.
- **Una API key de Gemini:** es la credencial que autoriza las consultas al servicio.
- **Conexión a internet:** necesaria para instalar dependencias y consultar la API.

En VS Code, abre **Terminal → Nueva terminal**.
Ejecuta los comandos correspondientes a tu sistema operativo, uno por uno.

### Para Windows — PowerShell

1. Descarga el proyecto y entra en su carpeta:

```powershell
git clone https://github.com/KennyLincoln/ProyectoIA.git
cd ProyectoIA
```

2. Crea y activa un entorno virtual:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

El entorno virtual mantiene las librerías de este proyecto separadas
de las utilizadas por otros proyectos. Al activarlo, aparecerá
`(venv)` al inicio de la terminal.

3. Instala las dependencias y crea el archivo de configuración:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

### Para macOS / Linux / WSL

1. Descarga el proyecto y entra en su carpeta:

```bash
git clone https://github.com/KennyLincoln/ProyectoIA.git
cd ProyectoIA
```

2. Crea y activa un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias y crea el archivo de configuración:

```bash
python -m pip install -r requirements.txt
cp .env.example .env
```

### Configurar la API key

Abre el archivo `.env` en VS Code y escribe tu clave de Gemini:

```dotenv
GEMINI_API_KEY=tu_clave_de_gemini
```

Reemplaza `tu_clave_de_gemini` por tu credencial real y guarda el archivo.

La plantilla `.env.example` debe contener el mismo nombre de variable,
pero sin una clave real:

```dotenv
GEMINI_API_KEY=
```

El archivo `.env` es personal y debe permanecer excluido de GitHub
mediante `.gitignore`.

## Cómo ejecutar el proyecto

Mantén el entorno virtual activado y ejecuta los comandos desde la
carpeta principal del proyecto, donde está este README.

### Probar las preguntas de WATERisLIFE

```bash
python src/consistencia.py
```

El programa envía tres preguntas de prueba: una sobre donaciones,
otra sobre impacto y otra sobre transparencia. Cada pregunta se
prueba tres veces.

La terminal muestra cuántas respuestas cumplieron la validación.
El resultado obtenido en la prueba con `gemini-3.5-flash-lite` fue:

```text
Donaciones: 3/3 respuestas válidas
Impacto: 3/3 respuestas válidas
Transparencia: 3/3 respuestas válidas
```

Los resultados se guardan en:

`src/prompts/registro_resultados.json`

Si el programa termina con un error, revisa la salida de la terminal:
el archivo JSON podría conservar los resultados de una ejecución anterior.

### Comparar los modelos

```bash
python src/evaluacion_modelos.py
```

Este programa realiza cuatro solicitudes por modelo y muestra:

- La respuesta generada.
- La latencia: cuánto tarda en responder.
- El costo estimado de la solicitud.
- Los promedios de las solicitudes exitosas.

## Estructura de carpetas y archivos

| Archivo o carpeta | Para qué sirve |
|---|---|
| `src/consumir_gemini.py` | Prepara solicitudes, consulta la API y procesa sus respuestas. |
| `src/consistencia.py` | Comprueba las respuestas del banco de prompts. |
| `src/evaluacion_modelos.py` | Compara el tiempo de respuesta y costo de los modelos. |
| `src/prompts/` | Contiene las instrucciones para la IA y los resultados de las pruebas. |
| `docs/` | Contiene el diagrama de arquitectura y las decisiones técnicas. |
| `tests/` | Carpeta reservada para pruebas del proyecto. |
| `requirements.txt` | Lista las librerías que necesita el programa. |
| `.env.example` | Muestra qué variables de configuración se necesitan, sin claves reales. |
| `.gitignore` | Indica qué archivos y carpetas no deben subirse a GitHub. |

El módulo de consumo de API separa tres funciones principales:

- `armar_peticion`: prepara la solicitud.
- `enviar_peticion`: envía la solicitud a Gemini.
- `extraer_texto`: obtiene el texto generado por el modelo.

La función `parsear_respuestas_json` permite procesar y validar
la estructura de la respuesta.

[Ver diagrama de arquitectura](docs/diagrama_arquitectura.png)

## Actualización de la elección de modelo para el Gate 1

El documento [decision-arquitectura.md](docs/decision-arquitectura.md)
se conserva como evidencia de la actividad Core entregada.

Este README registra una comparación posterior y la elección actualizada
del modelo para el banco de prompts de WIL.

### Comparación realizada

Se realizaron cuatro solicitudes por modelo, usando la misma pregunta
y la misma instrucción de sistema.

La pregunta utilizada fue: `¿Cual es la latencia`.

| Criterio | gemini-3.6-flash | gemini-3.5-flash-lite |
|---|---|---|
| Entrada: USD por millón de tokens de texto | 0.75 | 0.30 |
| Salida: USD por millón de tokens, incluyendo razonamiento | 3.75 | 2.50 |
| Latencia promedio informada por el programa | 8.37 segundos | 2.38 segundos |
| Costo promedio estimado por solicitud | USD 0.001506 | USD 0.000102 |
| Solicitudes exitosas | 4 de 4 | 4 de 4 |
| Calidad observada | Respuestas claras y relacionadas con la pregunta | Respuestas claras y relacionadas con la pregunta |

**Fuente de las tarifas:**

[Google — Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing)

Los costos son estimaciones calculadas con las tarifas de
**Standard, Paid Tier**. No representan necesariamente cargos
realizados en la cuenta utilizada.

### Modelo seleccionado

Elegí **gemini-3.5-flash-lite** porque, en esta prueba,
respondió más rápido y presentó un menor costo estimado.

Ambos modelos completaron las cuatro solicitudes. Además, Lite
obtuvo nueve respuestas válidas de nueve intentos en la prueba
independiente del banco de prompts de WATERisLIFE.

### Limitaciones

La comparación incluyó solamente cuatro solicitudes por modelo y una
pregunta general sobre latencia. Por lo tanto, sus resultados no
garantizan el mismo rendimiento en todas las situaciones.

La prueba del banco de prompts comprueba la estructura JSON de las
respuestas; no demuestra por sí sola que toda la información generada
sea correcta.

## Reglas que se mantienen durante todo el programa

- Ninguna contraseña, API key o token real debe subirse a GitHub.
- `.env` y el entorno virtual deben estar excluidos mediante `.gitignore`.
- `.env.example` se comparte sin credenciales reales.
- Cada proyecto utiliza su propio entorno virtual.
- Las librerías necesarias deben registrarse en `requirements.txt`.
- Los cambios del proyecto deben quedar registrados en Git.

## Registro del ensayo de instalación limpia

### Registro del 24/10/2026

- **Encontrado:** el archivo `cliente.py` correspondía a una unidad
  posterior y quedaba fuera del alcance de esta entrega.
- **Corregido:** se retiró `cliente.py` de la entrega del Gate 1.
- **Resultado confirmado:** el repositorio se clonó satisfactoriamente.

### Comprobaciones realizadas durante la preparación

En el entorno de trabajo se comprobó lo siguiente:

- La librería `python-dotenv` se importa correctamente.
- El programa encuentra la variable `GEMINI_API_KEY`.
- Los tres prompts de WATERisLIFE obtuvieron 3/3 respuestas válidas cada uno.
- La comparación actualizada completó cuatro solicitudes por cada modelo.

Estas comprobaciones corresponden al entorno de trabajo.
Para completar el ensayo de instalación limpia, falta verificar y
registrar la instalación y ejecución en una copia nueva del repositorio,
siguiendo únicamente las instrucciones de este README.

**Estado del ensayo completo: pendiente de verificación documentada.**