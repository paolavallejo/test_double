# src/order_service.py
class OrderService:
    def __init__(self, gateway, emailer, logger):
        self.gateway = gateway
        self.emailer = emailer
        self.logger = logger

    def create_order(self, email: str, amount: int) -> str:
        self.logger.log(f"Creating order for {email} amount={amount}")
        res = self.gateway.process(amount)
        if res.get("status") == "APPROVED":
            self.emailer.send(email, "Thanks", "Your order is approved")
            return "ORDER_APPROVED"
        return "ORDER_REJECTED"
        