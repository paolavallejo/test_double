class EmailServiceMock:
    def __init__(self):
        self.calls = 0

    def send(self, email):
        self.calls += 1

email_mock = EmailServiceMock()
service = OrderService(gateway_stub, dummy_logger, email_mock)

service.create_order(100)

assert email_mock.calls == 1
