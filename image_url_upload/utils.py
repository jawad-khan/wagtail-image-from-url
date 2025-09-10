import os
import uuid
import ipaddress
import socket
import requests
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from wagtail.images import get_image_model
from PIL import Image

ALLOWED_FORMATS = {"avif", "gif", "jpeg", "jpg", "png", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
TIMEOUT = (5, 15)  # connect, read


def _is_private_address(hostname: str) -> bool:
    """Prevent SSRF by blocking private/loopback/reserved IPs."""
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
    """Lightweight pre-check before downloading the whole file."""
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValidationError("Only http/https URLs are allowed.")

    if not parsed.hostname or _is_private_address(parsed.hostname):
        raise ValidationError("Blocked for security reasons (private/loopback address).")

    try:
        head = requests.head(url, allow_redirects=True, timeout=TIMEOUT)
        content_type = head.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            raise ValidationError("URL does not point to an image.")
    except requests.RequestException:
        raise ValidationError("Could not fetch image headers.")


def get_image_from_url(url, user=None):
    """
    Download the image securely, enforce size + format, save into Wagtail.
    """
    parsed = urlparse(url)

    # Enforce SSRF safety again
    if _is_private_address(parsed.hostname):
        raise ValidationError("Blocked for security reasons (private/loopback address).")

    # Stream the response with size check
    response = requests.get(url, stream=True, timeout=TIMEOUT)
    response.raise_for_status()

    content = b""
    for chunk in response.iter_content(1024 * 1024):  # 1MB chunks
        content += chunk
        if len(content) > MAX_FILE_SIZE:
            raise ValidationError("Image too large (max 10 MB).")

    # Validate with Pillow
    try:
        img = Image.open(ContentFile(content))
        img.verify()
        fmt = img.format.lower()
    except Exception:
        raise ValidationError("The file is not a valid image.")

    if fmt not in ALLOWED_FORMATS:
        raise ValidationError(f"Unsupported format: {fmt.upper()}")

    # Save to Wagtail Image model
    ImageModel = get_image_model()
    filename = f"{uuid.uuid4().hex}.{fmt or 'jpg'}"

    image = ImageModel.objects.create(
        title=os.path.basename(parsed.path) or "Imported image",
        file=ContentFile(content, name=filename),
        uploaded_by_user=user,
    )
    return image, fmt 
