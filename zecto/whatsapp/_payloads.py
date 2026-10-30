from __future__ import annotations

import copy
import re
from typing import Any

from ..exceptions import InvalidRequestError

Payload = dict[str, Any]


def _digits_only(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")


def _fill_wa_ids(contacts_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for contact in contacts_list:
        for phone in contact.get("phones", []) or []:
            if not phone.get("wa_id") and phone.get("phone"):
                phone["wa_id"] = _digits_only(phone["phone"])
    return contacts_list


def _base(phone_number_id: str, to: str, msg_type: str, reply_to: str | None = None) -> Payload:
    payload: Payload = {"phone_number_id": phone_number_id, "to": to, "type": msg_type}
    if reply_to:
        payload["context"] = {"message_id": reply_to}
    return payload


def _media_object(
    link: str | None,
    media_id: str | None,
    caption: str | None = None,
    filename: str | None = None,
) -> Payload:
    if not link and not media_id:
        raise InvalidRequestError("Provide either 'link' or 'media_id'")
    obj: Payload = {}
    if link:
        obj["link"] = link
    if media_id:
        obj["id"] = media_id
    if caption is not None:
        obj["caption"] = caption
    if filename is not None:
        obj["filename"] = filename
    return obj


def text(
    phone_number_id: str,
    to: str,
    body: str,
    preview_url: bool = False,
    reply_to: str | None = None,
) -> Payload:
    payload = _base(phone_number_id, to, "text", reply_to)
    payload["text"] = {"body": body, "preview_url": preview_url}
    return payload


def image(
    phone_number_id: str,
    to: str,
    link: str | None = None,
    media_id: str | None = None,
    caption: str | None = None,
    reply_to: str | None = None,
) -> Payload:
    payload = _base(phone_number_id, to, "image", reply_to)
    payload["image"] = _media_object(link, media_id, caption)
    return payload


def video(
    phone_number_id: str,
    to: str,
    link: str | None = None,
    media_id: str | None = None,
    caption: str | None = None,
    reply_to: str | None = None,
) -> Payload:
    payload = _base(phone_number_id, to, "video", reply_to)
    payload["video"] = _media_object(link, media_id, caption)
    return payload


def audio(
    phone_number_id: str,
    to: str,
    link: str | None = None,
    media_id: str | None = None,
    reply_to: str | None = None,
) -> Payload:
    payload = _base(phone_number_id, to, "audio", reply_to)
    payload["audio"] = _media_object(link, media_id)
    return payload


def document(
    phone_number_id: str,
    to: str,
    link: str | None = None,
    media_id: str | None = None,
    caption: str | None = None,
    filename: str | None = None,
    reply_to: str | None = None,
) -> Payload:
    payload = _base(phone_number_id, to, "document", reply_to)
    payload["document"] = _media_object(link, media_id, caption, filename)
    return payload


def location(
    phone_number_id: str,
    to: str,
    latitude: float,
    longitude: float,
    name: str | None = None,
    address: str | None = None,
    reply_to: str | None = None,
) -> Payload:
    payload = _base(phone_number_id, to, "location", reply_to)
    loc: Payload = {"latitude": latitude, "longitude": longitude}
    if name is not None:
        loc["name"] = name
    if address is not None:
        loc["address"] = address
    payload["location"] = loc
    return payload


def contacts(
    phone_number_id: str,
    to: str,
    contacts_list: list[dict[str, Any]],
    reply_to: str | None = None,
) -> Payload:
    payload = _base(phone_number_id, to, "contacts", reply_to)
    payload["contacts"] = _fill_wa_ids(copy.deepcopy(contacts_list))
    return payload


def interactive(
    phone_number_id: str,
    to: str,
    interactive_obj: dict[str, Any],
    reply_to: str | None = None,
) -> Payload:
    payload = _base(phone_number_id, to, "interactive", reply_to)
    payload["interactive"] = interactive_obj
    return payload


def _interactive_shell(
    itype: str,
    body: str,
    header: str | None = None,
    footer: str | None = None,
) -> Payload:
    obj: Payload = {"type": itype, "body": {"text": body}}
    if header is not None:
        obj["header"] = {"type": "text", "text": header}
    if footer is not None:
        obj["footer"] = {"text": footer}
    return obj


def _slugify_id(title: str | None, index: int) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", (title or "").lower()).strip("_")
    return base or f"option_{index}"


def interactive_buttons(
    phone_number_id: str,
    to: str,
    body: str,
    buttons: list[str | dict[str, Any]],
    header: str | None = None,
    footer: str | None = None,
    reply_to: str | None = None,
) -> Payload:
    if not buttons:
        raise InvalidRequestError("At least one button is required")
    if len(buttons) > 3:
        raise InvalidRequestError("A maximum of 3 reply buttons is allowed")

    action_buttons = []
    for i, b in enumerate(buttons):
        title: str | None
        if isinstance(b, str):
            bid, title = _slugify_id(b, i), b
        else:
            title = b.get("title")
            bid = b.get("id") or _slugify_id(title, i)
        if not title:
            raise InvalidRequestError(f"Button {i + 1}: title is required")
        action_buttons.append({"type": "reply", "reply": {"id": bid, "title": title}})

    obj = _interactive_shell("button", body, header, footer)
    obj["action"] = {"buttons": action_buttons}
    return interactive(phone_number_id, to, obj, reply_to)


def interactive_list(
    phone_number_id: str,
    to: str,
    body: str,
    button: str,
    sections: list[dict[str, Any]],
    header: str | None = None,
    footer: str | None = None,
    reply_to: str | None = None,
) -> Payload:
    if not button:
        raise InvalidRequestError("A menu 'button' label is required")
    if not sections:
        raise InvalidRequestError("At least one section is required")

    norm_sections = []
    for si, section in enumerate(sections):
        rows = section.get("rows") or []
        if not rows:
            raise InvalidRequestError(f"Section {si + 1}: at least one row is required")
        norm_rows = []
        for ri, row in enumerate(rows):
            title: str | None
            desc: str | None
            if isinstance(row, str):
                rid, title, desc = _slugify_id(row, ri), row, None
            else:
                title = row.get("title")
                rid = row.get("id") or _slugify_id(title, ri)
                desc = row.get("description")
            if not title:
                raise InvalidRequestError(f"Section {si + 1} row {ri + 1}: title is required")
            nr: Payload = {"id": rid, "title": title}
            if desc is not None:
                nr["description"] = desc
            norm_rows.append(nr)
        ns: Payload = {"rows": norm_rows}
        if section.get("title") is not None:
            ns["title"] = section["title"]
        norm_sections.append(ns)

    obj = _interactive_shell("list", body, header, footer)
    obj["action"] = {"button": button, "sections": norm_sections}
    return interactive(phone_number_id, to, obj, reply_to)


def interactive_cta_url(
    phone_number_id: str,
    to: str,
    body: str,
    display_text: str,
    url: str,
    header: str | None = None,
    footer: str | None = None,
    reply_to: str | None = None,
) -> Payload:
    if not display_text:
        raise InvalidRequestError("'display_text' is required")
    if not url:
        raise InvalidRequestError("'url' is required")

    obj = _interactive_shell("cta_url", body, header, footer)
    obj["action"] = {"name": "cta_url", "parameters": {"display_text": display_text, "url": url}}
    return interactive(phone_number_id, to, obj, reply_to)


def template(
    phone_number_id: str,
    to: str,
    template_id: str,
    body: Any = None,
    header: Any = None,
    buttons: Any = None,
) -> Payload:
    payload: Payload = {
        "phone_number_id": phone_number_id,
        "to": to,
        "template_id": template_id,
    }
    if body is not None:
        payload["body"] = body if isinstance(body, list) else [body]
    if header is not None:
        payload["header"] = header
    if buttons is not None:
        payload["buttons"] = buttons if isinstance(buttons, list) else [buttons]
    return payload


def read_receipt(phone_number_id: str, message_id: str, typing: bool = False) -> Payload:
    return {
        "phone_number_id": phone_number_id,
        "message_id": message_id,
        "typing": typing,
    }
