from __future__ import annotations

from typing import TYPE_CHECKING

from .account import Account, AsyncAccount
from .flows import AsyncFlows, Flows
from .messages import AsyncMessages, Messages
from .numbers import AsyncNumbers, Numbers
from .templates import AsyncTemplates, Templates

if TYPE_CHECKING:
    from .._transport import AsyncTransport, SyncTransport


class WhatsApp:
    def __init__(self, transport: SyncTransport) -> None:
        self.messages = Messages(transport)
        self.templates = Templates(transport)
        self.numbers = Numbers(transport)
        self.account = Account(transport)
        self.flows = Flows(transport)


class AsyncWhatsApp:
    def __init__(self, transport: AsyncTransport) -> None:
        self.messages = AsyncMessages(transport)
        self.templates = AsyncTemplates(transport)
        self.numbers = AsyncNumbers(transport)
        self.account = AsyncAccount(transport)
        self.flows = AsyncFlows(transport)
