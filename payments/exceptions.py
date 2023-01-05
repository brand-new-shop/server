from uuid import UUID


class CoinbasePaymentNotFoundError(Exception):
    def __init__(self, *, payment_uuid: UUID):
        super().__init__(f'Payment by ID {str(payment_uuid)} is not found')
        self.payment_uuid = payment_uuid
