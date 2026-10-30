from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from ..exceptions import InvalidRequestError

if TYPE_CHECKING:
    from .._transport import AsyncTransport, SyncTransport


class Flows:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list(self, status: str | None = None) -> Any:
        params = {"status": status}
        return self._transport.request("GET", "/v1/flows", params=params)

    def rename(self, flow_id: str, name: str) -> dict[str, Any]:
        if not flow_id:
            raise InvalidRequestError("flow_id is required")
        if not name:
            raise InvalidRequestError("name is required")
        return self._transport.request("POST", f"/v1/flows/{quote(str(flow_id), safe='')}/rename", json={"name": name})

    def set_status(self, flow_id: str, status: str) -> dict[str, Any]:
        if not flow_id:
            raise InvalidRequestError("flow_id is required")
        if not status:
            raise InvalidRequestError("status is required")
        return self._transport.request("POST", f"/v1/flows/{quote(str(flow_id), safe='')}/status", json={"status": status})

    def trigger(self, flow_id: str, to: str) -> dict[str, Any]:
        if not flow_id:
            raise InvalidRequestError("flow_id is required")
        if not to:
            raise InvalidRequestError("to is required")
        return self._transport.request("POST", f"/v1/flows/{quote(str(flow_id), safe='')}/trigger", json={"to": to})


class AsyncFlows:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list(self, status: str | None = None) -> Any:
        params = {"status": status}
        return await self._transport.request("GET", "/v1/flows", params=params)

    async def rename(self, flow_id: str, name: str) -> dict[str, Any]:
        if not flow_id:
            raise InvalidRequestError("flow_id is required")
        if not name:
            raise InvalidRequestError("name is required")
        return await self._transport.request("POST", f"/v1/flows/{quote(str(flow_id), safe='')}/rename", json={"name": name})

    async def set_status(self, flow_id: str, status: str) -> dict[str, Any]:
        if not flow_id:
            raise InvalidRequestError("flow_id is required")
        if not status:
            raise InvalidRequestError("status is required")
        return await self._transport.request("POST", f"/v1/flows/{quote(str(flow_id), safe='')}/status", json={"status": status})

    async def trigger(self, flow_id: str, to: str) -> dict[str, Any]:
        if not flow_id:
            raise InvalidRequestError("flow_id is required")
        if not to:
            raise InvalidRequestError("to is required")
        return await self._transport.request("POST", f"/v1/flows/{quote(str(flow_id), safe='')}/trigger", json={"to": to})
