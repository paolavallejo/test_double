class InMemoryPaymentGateway:
    def __init__(self): self.balance = 1000
    def process(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return {"status": "APPROVED"}
        return {"status": "REJECTED"}

from faker import Faker
fake = Faker()
email = fake.email()

