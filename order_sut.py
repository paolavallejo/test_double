# order_sut.py
def process_order(email, amount, logger, payment, emailer):
    """
    Lógica sencilla:
    1) Escribe log
    2) Pregunta a la pasarela si aprueba el pago
    3) Si aprueba, envía correo de confirmación
    4) Retorna "APPROVED" o "REJECTED"
    """
    logger.log(f"start: {email} amount={amount}")
    status = payment.process(amount)
    if status == "APPROVED":
        emailer.send(email, subject="Thanks", body="Order approved")
    return status