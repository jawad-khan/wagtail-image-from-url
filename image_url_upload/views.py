import os
import imghdr
import uuid
import ipaddress
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from wagtail.images import get_image_model
from PIL import Image


ALLOWED_FORMATS = {"avif", "gif", "jpeg", "jpg", "png", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
TIMEOUT = (5, 15)  # (connect timeout, read timeout)


def _is_private_address(hostname: str) -> bool:
    """Prevent SSRF by blocking private / loopback IP addresses."""
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast
    except ValueError:
        import socket
        try:
            resolved = socket.gethostbyname(hostname)
            ip = ipaddress.ip_address(resolved)
            return ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast
        except Exception:
            return True  # fail safe: block unresolvable
    return False


def enforce_size_limit(content_length: int):
    """Reusable size check."""
    if content_length and content_length > MAX_FILE_SIZE:
        raise ValidationError(f"File size exceeds {MAX_FILE_SIZE // (1024 * 1024)} MB limit.")


def get_image_from_url(url, user=None):
    """
    Download an image from a remote URL, with security checks:
    - Block SSRF
    - Enforce max size
    - Validate actual image format
    """
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValidationError("Only http/https URLs are allowed.")

    if _is_private_address(parsed.hostname):
        raise ValidationError("Blocked for security reasons (private/loopback address).")

    # Stream response with chunk size validation
    response = requests.get(url, stream=True, timeout=TIMEOUT, verify=True)
    response.raise_for_status()

    # Enforce Content-Length header (if present)
    enforce_size_limit(int(response.headers.get("Content-Length", 0)))

    content = b""
    for chunk in response.iter_content(1024 * 1024):  # 1 MB chunks
        content += chunk
        enforce_size_limit(len(content))

    # Verify with Pillow
    try:
        img = Image.open(ContentFile(content))
        img.verify()
    except Exception:
        raise ValidationError("The file is not a valid image.")

    # Check allowed formats
    ext = imghdr.what(None, content) or (img.format.lower() if hasattr(img, "format") else None)
    if ext and ext.lower() not in ALLOWED_FORMATS:
        raise ValidationError(f"Unsupported format: {ext.upper()}")

    # Save to Wagtail Image model
    ImageModel = get_image_model()
    filename = f"{uuid.uuid4().hex}.{ext or 'jpg'}"

    image = ImageModel.objects.create(
        title=os.path.basename(parsed.path) or "Imported image",
        file=ContentFile(content, name=filename),
        uploaded_by_user=user,
    )
    return image
