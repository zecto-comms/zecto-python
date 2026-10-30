# Zecto Python SDK

The official Python client for the [Zecto](https://zecto.io) messaging API.

## Install

```bash
pip install zecto
```

Requires Python 3.9 or newer.

## Quick start

```python
from zecto import ZectoClient

with ZectoClient(api_key="YOUR_API_KEY") as client:
    client.whatsapp.messages.send_text(
        phone_number_id="YOUR_PHONE_NUMBER_ID",
        to="923001234567",
        body="Hello from Zecto",
    )
```

Create an API key in the Zecto dashboard. Keep it on your server and never ship it in browser or mobile code.

## Async

```python
import asyncio
from zecto import AsyncZectoClient

async def main():
    async with AsyncZectoClient(api_key="YOUR_API_KEY") as client:
        numbers = await client.whatsapp.numbers.list()
        print(numbers)

asyncio.run(main())
```

Every method on `ZectoClient` has the same name and arguments on `AsyncZectoClient`.

## WhatsApp

### Messages

```python
wa = client.whatsapp

wa.messages.send_text(phone_number_id, to, "Hi there")
wa.messages.send_image(phone_number_id, to, link="https://example.com/photo.jpg", caption="Our new menu")
wa.messages.send_document(phone_number_id, to, link="https://example.com/invoice.pdf", filename="invoice.pdf")
wa.messages.send_location(phone_number_id, to, latitude=24.8607, longitude=67.0011, name="Head office")

wa.messages.send_buttons(phone_number_id, to, body="Confirm your order?", buttons=["Yes", "No"])

wa.messages.send_cta_url(
    phone_number_id, to,
    body="Track your parcel",
    display_text="Open tracking",
    url="https://example.com/track/123",
)

wa.messages.mark_read(phone_number_id, message_id)

wa.messages.list(phone_number_id=phone_number_id, status="delivered", limit=20)
wa.messages.get(message_id)
```

Also available: `send_video`, `send_audio`, `send_contacts`, `send_list`, and `send(payload)` for a raw payload.

### Templates

```python
wa.templates.list(status="APPROVED")

# Shows which variables a template needs
wa.templates.example_config(template_id)

wa.messages.send_template(
    phone_number_id, to,
    template_id=template_id,
    body=["Ali", "ORD-1042"],
)
```

### Numbers, account and flows

```python
wa.numbers.list()
wa.numbers.get(phone_number_id)

wa.account.get()

wa.flows.list()
wa.flows.trigger(flow_id, to="923001234567")
wa.flows.set_status(flow_id, "published")  # draft, published or paused
wa.flows.rename(flow_id, "Welcome flow")
```

## Errors

Every error raised by the SDK is a subclass of `zecto.ZectoError`.

```python
from zecto import ZectoError, AuthenticationError, RateLimitError

try:
    wa.messages.send_text(phone_number_id, to, "Hi")
except AuthenticationError:
    print("Check your API key")
except RateLimitError:
    print("Slow down and retry later")
except ZectoError as e:
    print(e)
```

| Status | Exception |
|---|---|
| 400, 422 | `ValidationError` |
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 429 | `RateLimitError` |
| 502 | `UpstreamError` |
| other 5xx | `ServerError` |
| network failure | `APIConnectionError` |

API errors carry `status_code`, `detail` and the raw response `body`.

## Options

```python
ZectoClient(
    api_key="YOUR_API_KEY",
    timeout=30.0,  # seconds
)
```

## License

MIT
