class PaymentGatewayStub:
    def process(self, amount):
        return {"status": "APPROVED" if amount <= 200 else "REJECTED"}

        