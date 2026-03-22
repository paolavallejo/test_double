# tests/test_doubles.py
from unittest.mock import MagicMock
from src.order_service import OrderService

# 1) DUMMY: no hace nada; sólo relleno
class DummyLogger:
    def log(self, msg): pass  # Dummy: no-ops  [2](http://xunitpatterns.com/~gerard/xunitTutorialSlides-V1.pdf)

# 2) STUB: respuestas predefinidas para avanzar
class PaymentGatewayStub:
    def process(self, amount):  # Stub: respuestas predefinidas  [1](https://martinfowler.com/articles/mocksArentStubs.html)
        return {"status": "APPROVED" if amount <= 200 else "REJECTED"}

# 3) FAKE: lógica simple funcional (versión "en memoria")
def test_approved_order_uses_mock_emailer():
    email_mock = MagicMock()  # Mock: verificamos interacción  [3](https://docs.python.org/3/library/unittest.mock.html)
    service = OrderService(PaymentGatewayStub(), email_mock, DummyLogger())
    result = service.create_order("user@example.com", 100)
    assert result == "ORDER_APPROVED"
    email_mock.send.assert_called_once()

# 4) SPY: registra qué pasó (sin expectativas previas)
def test_spy_records_arguments_with_pytest_mocker(mocker):
    class Emailer:
        def send(self, to, subject, body): pass
    emailer = Emailer()
    spy = mocker.spy(emailer, "send")  # Spy: registra llamadas  [4](https://pytest-mock.readthedocs.io/en/latest/usage.html)
    service = OrderService(PaymentGatewayStub(), emailer, DummyLogger())
    service.create_order("thanks@example.com", 50)
    spy.assert_called_once()
    assert spy.call_args[0][0] == "thanks@example.com"