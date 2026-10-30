from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from . import _payloads
from ..exceptions import InvalidRequestError

if TYPE_CHECKING:
    from .._transport import AsyncTransport, SyncTransport


class Messages:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def send(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._transport.request("POST", "/v1/messages/send", json=payload)

    def send_text(
        self,
        phone_number_id: str,
        to: str,
        body: str,
        preview_url: bool = False,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.text(phone_number_id, to, body, preview_url, reply_to)
        return self.send(payload)

    def send_image(
        self,
        phone_number_id: str,
        to: str,
        link: str | None = None,
        media_id: str | None = None,
        caption: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.image(phone_number_id, to, link, media_id, caption, reply_to)
        return self.send(payload)

    def send_video(
        self,
        phone_number_id: str,
        to: str,
        link: str | None = None,
        media_id: str | None = None,
        caption: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.video(phone_number_id, to, link, media_id, caption, reply_to)
        return self.send(payload)

    def send_audio(
        self,
        phone_number_id: str,
        to: str,
        link: str | None = None,
        media_id: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.audio(phone_number_id, to, link, media_id, reply_to)
        return self.send(payload)

    def send_document(
        self,
        phone_number_id: str,
        to: str,
        link: str | None = None,
        media_id: str | None = None,
        caption: str | None = None,
        filename: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.document(phone_number_id, to, link, media_id, caption, filename, reply_to)
        return self.send(payload)

    def send_location(
        self,
        phone_number_id: str,
        to: str,
        latitude: float,
        longitude: float,
        name: str | None = None,
        address: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.location(phone_number_id, to, latitude, longitude, name, address, reply_to)
        return self.send(payload)

    def send_contacts(
        self,
        phone_number_id: str,
        to: str,
        contacts: list[dict[str, Any]],
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.contacts(phone_number_id, to, contacts, reply_to)
        return self.send(payload)

    def send_buttons(
        self,
        phone_number_id: str,
        to: str,
        body: str,
        buttons: list[str | dict[str, Any]],
        header: str | None = None,
        footer: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.interactive_buttons(phone_number_id, to, body, buttons, header, footer, reply_to)
        return self.send(payload)

    def send_list(
        self,
        phone_number_id: str,
        to: str,
        body: str,
        button: str,
        sections: list[dict[str, Any]],
        header: str | None = None,
        footer: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.interactive_list(phone_number_id, to, body, button, sections, header, footer, reply_to)
        return self.send(payload)

    def send_cta_url(
        self,
        phone_number_id: str,
        to: str,
        body: str,
        display_text: str,
        url: str,
        header: str | None = None,
        footer: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.interactive_cta_url(phone_number_id, to, body, display_text, url, header, footer, reply_to)
        return self.send(payload)

    def send_template(
        self,
        phone_number_id: str,
        to: str,
        template_id: str,
        body: Any = None,
        header: Any = None,
        buttons: Any = None,
    ) -> dict[str, Any]:
        payload = _payloads.template(phone_number_id, to, template_id, body, header, buttons)
        return self._transport.request("POST", "/v1/messages/send-template", json=payload)

    def mark_read(self, phone_number_id: str, message_id: str, typing: bool = False) -> dict[str, Any]:
        payload = _payloads.read_receipt(phone_number_id, message_id, typing)
        return self._transport.request("POST", "/v1/messages/read", json=payload)

    def list(
        self,
        phone_number_id: str | None = None,
        status: str | None = None,
        to_number: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Any:
        params = {
            "phone_number_id": phone_number_id,
            "status": status,
            "to_number": to_number,
            "limit": limit,
            "offset": offset,
        }
        return self._transport.request("GET", "/v1/messages", params=params)

    def get(self, message_id: str) -> dict[str, Any]:
        if not message_id:
            raise InvalidRequestError("message_id is required")
        return self._transport.request("GET", f"/v1/messages/{quote(str(message_id), safe='')}")


class AsyncMessages:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def send(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._transport.request("POST", "/v1/messages/send", json=payload)

    async def send_text(
        self,
        phone_number_id: str,
        to: str,
        body: str,
        preview_url: bool = False,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.text(phone_number_id, to, body, preview_url, reply_to)
        return await self.send(payload)

    async def send_image(
        self,
        phone_number_id: str,
        to: str,
        link: str | None = None,
        media_id: str | None = None,
        caption: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.image(phone_number_id, to, link, media_id, caption, reply_to)
        return await self.send(payload)

    async def send_video(
        self,
        phone_number_id: str,
        to: str,
        link: str | None = None,
        media_id: str | None = None,
        caption: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.video(phone_number_id, to, link, media_id, caption, reply_to)
        return await self.send(payload)

    async def send_audio(
        self,
        phone_number_id: str,
        to: str,
        link: str | None = None,
        media_id: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.audio(phone_number_id, to, link, media_id, reply_to)
        return await self.send(payload)

    async def send_document(
        self,
        phone_number_id: str,
        to: str,
        link: str | None = None,
        media_id: str | None = None,
        caption: str | None = None,
        filename: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.document(phone_number_id, to, link, media_id, caption, filename, reply_to)
        return await self.send(payload)

    async def send_location(
        self,
        phone_number_id: str,
        to: str,
        latitude: float,
        longitude: float,
        name: str | None = None,
        address: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.location(phone_number_id, to, latitude, longitude, name, address, reply_to)
        return await self.send(payload)

    async def send_contacts(
        self,
        phone_number_id: str,
        to: str,
        contacts: list[dict[str, Any]],
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.contacts(phone_number_id, to, contacts, reply_to)
        return await self.send(payload)

    async def send_buttons(
        self,
        phone_number_id: str,
        to: str,
        body: str,
        buttons: list[str | dict[str, Any]],
        header: str | None = None,
        footer: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.interactive_buttons(phone_number_id, to, body, buttons, header, footer, reply_to)
        return await self.send(payload)

    async def send_list(
        self,
        phone_number_id: str,
        to: str,
        body: str,
        button: str,
        sections: list[dict[str, Any]],
        header: str | None = None,
        footer: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.interactive_list(phone_number_id, to, body, button, sections, header, footer, reply_to)
        return await self.send(payload)

    async def send_cta_url(
        self,
        phone_number_id: str,
        to: str,
        body: str,
        display_text: str,
        url: str,
        header: str | None = None,
        footer: str | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        payload = _payloads.interactive_cta_url(phone_number_id, to, body, display_text, url, header, footer, reply_to)
        return await self.send(payload)

    async def send_template(
        self,
        phone_number_id: str,
        to: str,
        template_id: str,
        body: Any = None,
        header: Any = None,
        buttons: Any = None,
    ) -> dict[str, Any]:
        payload = _payloads.template(phone_number_id, to, template_id, body, header, buttons)
        return await self._transport.request("POST", "/v1/messages/send-template", json=payload)

    async def mark_read(self, phone_number_id: str, message_id: str, typing: bool = False) -> dict[str, Any]:
        payload = _payloads.read_receipt(phone_number_id, message_id, typing)
        return await self._transport.request("POST", "/v1/messages/read", json=payload)

    async def list(
        self,
        phone_number_id: str | None = None,
        status: str | None = None,
        to_number: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Any:
        params = {
            "phone_number_id": phone_number_id,
            "status": status,
            "to_number": to_number,
            "limit": limit,
            "offset": offset,
        }
        return await self._transport.request("GET", "/v1/messages", params=params)

    async def get(self, message_id: str) -> dict[str, Any]:
        if not message_id:
            raise InvalidRequestError("message_id is required")
        return await self._transport.request("GET", f"/v1/messages/{quote(str(message_id), safe='')}")
