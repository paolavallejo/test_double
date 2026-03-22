class EmailServiceSpy:
    def __init__(self):
        self.sent_emails = []

    def send(self, email):
        self.sent_emails.append(email)
        