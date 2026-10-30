from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from ..exceptions import InvalidRequestError

if TYPE_CHECKING:
    from .._transport import AsyncTransport, SyncTransport


class Templates:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(
        self,
        status: str | None = None,
        category: str | None = None,
        search: str | None = None,
    ) -> Any:
        params = {"status": status, "category": category, "search": search}
        return self._transport.request("GET", "/v1/templates", params=params)

    def example_config(self, template_id: str) -> dict[str, Any]:
        if not template_id:
            raise InvalidRequestError("template_id is required")
        return self._transport.request("GET", f"/v1/templates/example-config/{quote(str(template_id), safe='')}")


class AsyncTemplates:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(
        self,
        status: str | None = None,
        category: str | None = None,
        search: str | None = None,
    ) -> Any:
        params = {"status": status, "category": category, "search": search}
        return await self._transport.request("GET", "/v1/templates", params=params)

    async def example_config(self, template_id: str) -> dict[str, Any]:
        if not template_id:
            raise InvalidRequestError("template_id is required")
        return await self._transport.request("GET", f"/v1/templates/example-config/{quote(str(template_id), safe='')}")
