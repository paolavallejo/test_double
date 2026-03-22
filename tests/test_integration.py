# tests/test_integration.py
from src.order_service import OrderService
from faker import Faker  # Datos realistas  [5](https://faker.readthedocs.io/)

class DummyLogger:
    def log(self, msg): pass

class InMemoryPaymentGateway:  # Fake funcional  [1](https://martinfowler.com/articles/mocksArentStubs.html)
    def __init__(self): self.balance = 1000
    def process(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return {"status": "APPROVED"}
        return {"status": "REJECTED"}

class EmailRecorder:  # Spy manual (registro simple)
    def __init__(self): self.sent = []
    def send(self, to, subject, body): self.sent.append((to, subject, body))

def test_integration_with_fake_gateway_and_spy():
    fake = Faker()
    email = fake.email()  # Faker  [5](https://faker.readthedocs.io/)
    spy = EmailRecorder()
    service = OrderService(InMemoryPaymentGateway(), spy, DummyLogger())
    result = service.create_order(email, 120)
    assert result == "ORDER_APPROVED"
    assert spy.sent and spy.sent[0][0] == email