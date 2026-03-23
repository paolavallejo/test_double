# test_01_con_errores.py
"""
FALLA INTENCIONAL (sin pytest.raises).
Dejamos que las excepciones se propaguen.
"""

from order_sut import process_order


def test_logger_inexistente_rompe():
    """
    Caso: logger=None -> process_order intenta logger.log(...) -> AttributeError.
    Deja que la excepción explote para mostrar el traceback en rojo.
    Solución (en test_02): DummyLogger.
    """
    process_order("a@b.com", 50, logger=None, payment=None, emailer=None)
    # Si por alguna razón no explotara, forzamos el fallo (defensivo).
    assert False, "Esperaba AttributeError por logger None (usa DummyLogger en soluciones)."


def test_payment_real_inaccesible():
    """
    Caso: 'payment' simula una dependencia externa que falla (red/BD).
    Deja que el TimeoutError explote. Ilustra por qué necesitamos Stub/Fake.
    """
    class RealPayment:
        def process(self, amount):
            # Simula red/BD inestable o costosa
            raise TimeoutError("No se pudo contactar la pasarela")

    logger = type("L", (), {"log": print})()
    process_order("a@b.com", 50, logger=logger, payment=RealPayment(), emailer=None)
    assert False, "Esperaba TimeoutError por dependencia externa (usa Stub/Fake en soluciones)."


def test_envio_email_real_indeseado():
    """
    Caso: EmailService 'real' que podría enviar correos.
    Forzamos un RuntimeError para evidenciar el efecto colateral no deseado.
    """
    class RealEmailer:
        def send(self, *args, **kwargs):
            raise RuntimeError("Intento de enviar correo real (bloqueado)")

    class OkPayment:
        def process(self, amount):
            return "APPROVED"

    logger = type("L", (), {"log": print})()
    process_order("a@b.com", 50, logger=logger, payment=OkPayment(), emailer=RealEmailer())
    assert False, "Esperaba RuntimeError al intentar enviar correo real (usa Mock en soluciones)."


def test_no_puedo_validar_interaccion_sin_mock():
    """
    Caso: no hay evidencia de que emailer.send() se haya llamado.
    Ejecuta el flujo y falla con un assert didáctico -> necesitamos Mock/Spy.
    """
    class SilentEmailer:
        def send(self, *args, **kwargs):
            pass

    class OkPayment:
        def process(self, amount):
            return "APPROVED"

    logger = type("L", (), {"log": print})()
    emailer = SilentEmailer()

    _ = process_order("a@b.com", 50, logger=logger, payment=OkPayment(), emailer=emailer)

    # Falla explícitamente: sin mock/spy no podemos probar interacción.
    assert False, (
        "No hay evidencia de interacción con emailer.send(). "
        "Usa Mock (assert_called*) o un Spy en test_02_con_soluciones.py."
    )


def test_datos_fijos_vuelven_fragil_el_test():
    """
    Caso: usar siempre el mismo email -> baja cobertura / fragilidad.
    Aunque el resultado sea 'APPROVED', forzamos FAIL para explicar por qué
    debemos variar datos (Faker/parametrize) en las soluciones.
    """
    class OkPayment:
        def process(self, amount):
            return "APPROVED"

    class SilentEmailer:
        def send(self, *args, **kwargs):
            pass

    logger = type("L", (), {"log": print})()
    email = "a@b.com"  # dato fijo -> fragilidad
    status = process_order(email, 50, logger=logger, payment=OkPayment(), emailer=SilentEmailer())

    # Aun si pasa la lógica, marcamos fallo didáctico por falta de variabilidad.
    assert status == "APPROVED", "Se esperaba APPROVED."
    assert False, (
        "Uso de dato fijo: prueba frágil y poca cobertura. "
        "Usa Faker o pytest.mark.parametrize en test_02_con_soluciones.py."
    )