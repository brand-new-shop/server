from rest_framework import status
from rest_framework.exceptions import APIException


class SupportTicketCreationRateLimitExceeded(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS

    def __init__(self, seconds_to_wait: int):
        super().__init__({'seconds_to_wait': seconds_to_wait})
