from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from ..exceptions import InvalidRequestError

if TYPE_CHECKING:
    from .._transport import AsyncTransport, SyncTransport


class Numbers:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(self) -> Any:
        return self._transport.request("GET", "/v1/numbers")

    def get(self, phone_number_id: str) -> dict[str, Any]:
        if not phone_number_id:
            raise InvalidRequestError("phone_number_id is required")
        return self._transport.request("GET", f"/v1/numbers/{quote(str(phone_number_id), safe='')}")


class AsyncNumbers:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(self) -> Any:
        return await self._transport.request("GET", "/v1/numbers")

    async def get(self, phone_number_id: str) -> dict[str, Any]:
        if not phone_number_id:
            raise InvalidRequestError("phone_number_id is required")
        return await self._transport.request("GET", f"/v1/numbers/{quote(str(phone_number_id), safe='')}")
