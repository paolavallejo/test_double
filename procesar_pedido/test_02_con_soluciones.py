# test_02_con_soluciones.py
import pytest
from unittest.mock import MagicMock
from order_sut import process_order

# ---------- DUMMY ----------
class DummyLogger:
    def log(self, msg):  # No hace nada; evita AttributeError y ruido
        pass

# ---------- STUB ----------
class StubPayment:
    # Devolvemos una respuesta controlada (sin red/BD)
    def process(self, amount):
        return "APPROVED" if amount <= 200 else "REJECTED"

# ---------- SPY ----------
class EmailSpy:
    def __init__(self): self.sent = []
    def send(self, email, subject, body):
        self.sent.append((email, subject, body))

# ---------- FAKE (opcional con estado) ----------
class InMemoryPaymentFake:
    def __init__(self, balance=300):
        self.balance = balance
    def process(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return "APPROVED"
        return "REJECTED"

# ============= SOLUCIONES A CADA ERROR =============

def test_sol_1_dummy_evita_attributeerror_logger():
    logger = DummyLogger()           # ✅ Dummy resuelve logger None
    payment = StubPayment()          # (todavía no importa)
    emailer = MagicMock()            # mock placeholder
    status = process_order("a@b.com", 50, logger, payment, emailer)
    assert status == "APPROVED"      # prueba se ejecuta sin romper por logger

def test_sol_2_stub_evita_red_y_controla_estado():
    logger = DummyLogger()
    payment = StubPayment()          # ✅ Stub evita Timeout y decide output
    emailer = MagicMock()
    assert process_order("a@b.com", 150, logger, payment, emailer) == "APPROVED"
    assert process_order("a@b.com", 250, logger, payment, emailer) == "REJECTED"

def test_sol_3_mock_evita_envio_real_y_verifica_interaccion():
    logger = DummyLogger()
    payment = StubPayment()
    emailer = MagicMock()            # ✅ Mock evita efectos reales y permite asserts
    process_order("a@b.com", 100, logger, payment, emailer)
    emailer.send.assert_called_once()                         # verificación de comportamiento
    emailer.send.assert_called_with("a@b.com", subject="Thanks", body="Order approved")

def test_sol_4_spy_inspecciona_argumentos():
    logger = DummyLogger()
    payment = StubPayment()
    emailer = EmailSpy()             # ✅ Spy registra llamadas y argumentos
    process_order("destino@x.com", 80, logger, payment, emailer)
    assert emailer.sent == [("destino@x.com", "Thanks", "Order approved")]

def test_sol_5_faker_datos_realistas_para_variedad():
    try:
        from faker import Faker      # ✅ Faker genera datos realistas
    except Exception:
        pytest.skip("Instala Faker para ejecutar esta prueba: pip install Faker")
    fake = Faker()

    logger = DummyLogger()
    payment = StubPayment()
    emailer = MagicMock()

    # ejecutamos con emails variados para evitar fragilidad
    emails = [fake.email() for _ in range(3)]
    for e in emails:
        status = process_order(e, 60, logger, payment, emailer)
        assert status == "APPROVED"
        emailer.send.assert_any_call(e, subject="Thanks", body="Order approved")

def test_bonus_fake_con_estado():
    logger = DummyLogger()
    payment = InMemoryPaymentFake(balance=200)  # ✅ Fake modela estado entre llamadas
    emailer = MagicMock()
    assert process_order("x@y.com", 150, logger, payment, emailer) == "APPROVED"
    assert process_order("x@y.com", 150, logger, payment, emailer) == "REJECTED"  # se consumió el "saldo"