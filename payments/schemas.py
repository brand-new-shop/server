from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CoinbaseCharge:
    uuid: UUID
    payment_amount: Decimal
    hosted_url: str
    status: str
    context: str | None
