from unittest.mock import patch, Mock
import pytest
from consumir_gemini import enviar_peticion

import cliente

@pytest.fixture(autouse=True)
def reiniciar_costo_total():
    cliente.costo_total_sesion = 0
    yield

# ================= TESTS ENVIAR PETICION =================

def test_enviar_peticion_credencial_invalida():
    respuesta_falsa = Mock(status_code=401)

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        with pytest.raises(ValueError):
            enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})


def test_enviar_peticion_sin_permiso():
    respuesta_falsa = Mock(status_code=403)

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        with pytest.raises(ValueError):
            enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})


def test_enviar_peticion_limite_de_uso():
    respuesta_falsa = Mock(status_code=429)

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        with pytest.raises(TimeoutError):
            enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})


def test_enviar_peticion_error_del_proveedor():
    respuesta_falsa = Mock(status_code=500)

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        with pytest.raises(TimeoutError):
            enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})


def test_enviar_peticion_exito():
    respuesta_falsa = Mock(status_code=200)
    respuesta_falsa.json.return_value = {"texto": "respuesta simulada"}

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        resultado = enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})

    assert resultado == {"texto": "respuesta simulada"}

# ================= TESTS REINTENTOS =================

def test_con_reintento_espera_entre_intentos():
    intentos = {"n": 0}

    def funcion_que_falla_una_vez():
        intentos["n"] += 1
        if intentos["n"] == 1:
            raise TimeoutError("simulado")
        return "ok"

    with patch("cliente.time.sleep") as mock_sleep:
        resultado = cliente.con_reintento(funcion_que_falla_una_vez)

    assert resultado == "ok"
    mock_sleep.assert_called_once()


def test_con_reintento_agota_intentos():
    def siempre_falla():
        raise TimeoutError("simulado")

    with patch("cliente.time.sleep"):
        with pytest.raises(TimeoutError):
            cliente.con_reintento(siempre_falla, intentos=3)


def test_con_reintento_no_reintenta_value_error():
    operacion = Mock(side_effect=ValueError("simulado"))

    with patch("cliente.time.sleep") as dormir:
        with pytest.raises(ValueError):
            cliente.con_reintento(operacion)

    operacion.assert_called_once()
    dormir.assert_not_called()

# ================= TESTS COSTO =================

def test_registrar_costo_calcula_costo_correcto():
    respuesta_falsa = {"usageMetadata": {"totalTokenCount": 1000}}

    costo = cliente.registrar_costo(respuesta_falsa)

    assert costo == cliente.COSTO_POR_1000_TOKENS


def test_registrar_costo_acumula():
    respuesta_falsa = {"usageMetadata": {"totalTokenCount": 1000}}

    cliente.registrar_costo(respuesta_falsa)

    assert cliente.costo_total_sesion == cliente.COSTO_POR_1000_TOKENS

# ================= TESTS CONSULTAR MODELO =================

def test_consultar_modelo_convierte_error():
    error_simulado = TimeoutError("simulado")

    with patch("cliente.time.sleep"):
        with patch("src.consumir_gemini.requests.post", side_effect=error_simulado):
            with pytest.raises(RuntimeError):
                cliente.consultar_modelo("Pregunta de prueba")


def test_consultar_modelo_propaga_value_error():
    respuesta_falsa = Mock(status_code=401)

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        with pytest.raises(ValueError):
            cliente.consultar_modelo("Pregunta de prueba")