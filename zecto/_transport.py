from __future__ import annotations

from typing import Any

import httpx

from .exceptions import APIConnectionError, error_for_status

BASE_URL = "https://api.zecto.io/whatsapp"
DEFAULT_TIMEOUT = 30.0


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    if not params:
        return None
    return {k: v for k, v in params.items() if v is not None}


def _format_detail(detail: Any) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        parts = []
        for item in detail:
            if isinstance(item, dict):
                loc = item.get("loc") or []
                if loc and loc[0] == "body":
                    loc = loc[1:]
                field = ".".join(str(p) for p in loc)
                msg = item.get("msg", "invalid")
                parts.append(f"{field}: {msg}" if field else msg)
            else:
                parts.append(str(item))
        return "; ".join(parts)
    return str(detail)


def _handle_response(resp: httpx.Response, method: str | None = None, path: str | None = None) -> Any:
    if 200 <= resp.status_code < 300:
        try:
            return resp.json()
        except ValueError:
            return {}

    try:
        body = resp.json()
    except ValueError:
        body = {}

    raw_detail = body.get("detail") or body.get("error") or resp.text or "Unknown error"
    detail = _format_detail(raw_detail)
    raise error_for_status(resp.status_code, detail, body, method=method, path=path)


def _headers(api_key: str) -> dict[str, str]:
    return {"X-API-Key": api_key, "Content-Type": "application/json"}


class SyncTransport:
    def __init__(
        self,
        api_key: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._client = httpx.Client(
            base_url=BASE_URL,
            headers=_headers(api_key),
            timeout=timeout,
        )

    def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        try:
            resp = self._client.request(method, path, params=_clean_params(params), json=json)
        except httpx.HTTPError as e:
            raise APIConnectionError(str(e)) from e
        return _handle_response(resp, method, path)

    def close(self) -> None:
        self._client.close()


class AsyncTransport:
    def __init__(
        self,
        api_key: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers=_headers(api_key),
            timeout=timeout,
        )

    async def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        try:
            resp = await self._client.request(method, path, params=_clean_params(params), json=json)
        except httpx.HTTPError as e:
            raise APIConnectionError(str(e)) from e
        return _handle_response(resp, method, path)

    async def close(self) -> None:
        await self._client.aclose()
