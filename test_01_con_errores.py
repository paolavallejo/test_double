# test_01_con_errores.py
import pytest
from order_sut import process_order

def test_logger_inexistente_rompe():  # ❌ ERROR REAL 1: logger es None
    # logger = None provoca AttributeError al llamar logger.log(...)
    with pytest.raises(AttributeError):
        process_order("a@b.com", 50, logger=None, payment=None, emailer=None)

def test_payment_real_inaccesible():  # ❌ ERROR REAL 2: payment real/externo
    class RealPayment:
        def process(self, amount):
            # Simula que intenta ir a la red/BD y falla
            raise TimeoutError("No se pudo contactar la pasarela")
    with pytest.raises(TimeoutError):
        process_order("a@b.com", 50, logger=type("L", (), {"log": print})(), payment=RealPayment(), emailer=None)

def test_envio_email_real_indeseado():  # ❌ ERROR REAL 3: email real
    class RealEmailer:
        def send(self, *args, **kwargs):
            raise RuntimeError("Intento de enviar correo real (bloqueado)")
    class OkPayment:
        def process(self, amount): return "APPROVED"

    with pytest.raises(RuntimeError):
        process_order("a@b.com", 50, logger=type("L", (), {"log": print})(), payment=OkPayment(), emailer=RealEmailer())

def test_no_puedo_validar_interaccion_sin_mock():  # ❌ ERROR REAL 4: no sé si se llamó send
    class SilentEmailer:
        def send(self, *args, **kwargs): pass
    class OkPayment:
        def process(self, amount): return "APPROVED"
    # Sin mock/spy no tenemos forma sencilla de afirmar "se llamó"
    # Forzamos un assert imposible para ilustrar el problema:
    emailer = SilentEmailer()
    status = process_order("a@b.com", 50, logger=type("L", (), {"log": print})(), payment=OkPayment(), emailer=emailer)
    assert False, "No tenemos evidencia de que emailer.send fue invocado; necesitamos un mock o un spy"

def test_datos_fijos_vuelven_fragil_el_test():  # ❌ ERROR REAL 5: datos poco variados
    class OkPayment:
        def process(self, amount): return "APPROVED"
    class SilentEmailer:
        def send(self, *args, **kwargs): pass

    email = "a@b.com"  # Siempre el mismo → baja cobertura y puede ocultar problemas
    status = process_order(email, 50, logger=type("L", (), {"log": print})(), payment=OkPayment(), emailer=SilentEmailer())
    assert status == "APPROVED"
