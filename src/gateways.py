# src/gateways.py
class PaymentGateway:
    def process(self, amount: int) -> dict:
        raise NotImplementedError
