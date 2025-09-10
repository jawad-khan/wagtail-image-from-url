import ipaddress
import socket
import requests
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.files.base import ContentFile

ALLOWED_FORMATS = {"avif", "gif", "jpeg", "jpg", "png", "webp"}
TIMEOUT = (5, 15)


def _is_private_address(hostname: str) -> bool:
    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        try:
            resolved = socket.gethostbyname(hostname)
            ip = ipaddress.ip_address(resolved)
        except Exception:
            return True
    return ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast


def validate_image_url(url: str):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValidationError("Only http/https URLs are allowed.")

    if not parsed.hostname or _is_private_address(parsed.hostname):
        raise ValidationError("Blocked for security reasons (private/loopback address).")

    # Quick HEAD check
    try:
        head = requests.head(url, allow_redirects=True, timeout=TIMEOUT)
        content_type = head.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            raise ValidationError("URL does not point to an image.")
    except requests.RequestException:
        raise ValidationError("Could not fetch image headers.")

    # Fetch first chunk to validate with Pillow
    try:
        response = requests.get(url, stream=True, timeout=TIMEOUT)
        response.raise_for_status()

        # Read a small chunk
        chunk = b"".join(next(response.iter_content(1024)) for _ in range(10))
        img = Image.open(ContentFile(chunk))
        fmt = img.format.lower()

        if fmt not in ALLOWED_FORMATS:
            raise ValidationError(f"Unsupported format: {fmt.upper()}")
    except Exception:
        raise ValidationError("Invalid or unsupported image URL.")
