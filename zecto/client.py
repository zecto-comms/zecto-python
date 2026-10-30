from __future__ import annotations

from ._transport import DEFAULT_TIMEOUT, AsyncTransport, SyncTransport
from .whatsapp import AsyncWhatsApp, WhatsApp


class ZectoClient:
    def __init__(
        self,
        api_key: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("api_key is required")
        if api_key != api_key.strip():
            raise ValueError("api_key must not have leading or trailing whitespace")
        self._transport = SyncTransport(api_key, timeout=timeout)
        self.whatsapp = WhatsApp(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> ZectoClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class AsyncZectoClient:
    def __init__(
        self,
        api_key: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("api_key is required")
        if api_key != api_key.strip():
            raise ValueError("api_key must not have leading or trailing whitespace")
        self._transport = AsyncTransport(api_key, timeout=timeout)
        self.whatsapp = AsyncWhatsApp(self._transport)

    async def close(self) -> None:
        await self._transport.close()

    async def __aenter__(self) -> AsyncZectoClient:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()
