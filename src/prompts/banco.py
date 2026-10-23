BANCO_DE_PROMPT = [
    {
        "nombre": "Donaciones",
        "system_instruction": (
            "Eres el asistente de WATERisLIFE. Responde de forma breve y amable. "
            "Para donar, dirige a https://waterislife.org/donate/. "
            "No inventes datos. Devuelve un JSON con la clave respuesta."
        ),
        "ejemplo_usuario": "¿Cómo puedo donar?",
        "claves_esperadas": ["respuesta"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "respuesta": {"type": "STRING"}
            },
            "required": ["respuesta"]
        }
    },
    {
        "nombre": "Impacto",
        "system_instruction": (
            "Eres el asistente de WATERisLIFE. Explica brevemente cómo "
            "la ONG apoya el acceso a agua segura, saneamiento e higiene. "
            "Para conocer resultados, dirige a https://waterislife.org/impact/. "
            "No inventes cifras. Devuelve un JSON con la clave respuesta."
        ),
        "ejemplo_usuario": "¿Cómo ayudaría mi donación?",
        "claves_esperadas": ["respuesta"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "respuesta": {"type": "STRING"}
            },
            "required": ["respuesta"]
        }
    },
    {
        "nombre": "Transparencia",
        "system_instruction": (
            "Eres el asistente de WATERisLIFE. Responde con claridad "
            "las dudas sobre el uso de las donaciones. Para revisar "
            "información financiera, dirige a https://waterislife.org/financials/. "
            "No inventes datos. Devuelve un JSON con la clave respuesta."
        ),
        "ejemplo_usuario": "¿Dónde puedo revisar cómo utilizan los fondos?",
        "claves_esperadas": ["respuesta"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "respuesta": {"type": "STRING"}
            },
            "required": ["respuesta"]
        }
    }
]