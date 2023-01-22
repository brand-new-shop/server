from rest_framework import status
from rest_framework.exceptions import APIException


class TicketIsClosed(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Ticket was closed, so now only read-only operations available'


class SupportTicketCreationRateLimitExceeded(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Ticket creation rate limit exceeded'

    def __init__(self, seconds_to_wait: int):
        super().__init__({'seconds_to_wait': seconds_to_wait})
