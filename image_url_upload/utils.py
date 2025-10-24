"""
Utility functions for image URL validation and download.

This module provides security-focused utilities for validating image URLs,
preventing SSRF attacks, and safely downloading images from external sources.
"""

import ipaddress
import logging
import os
import socket
import uuid
from typing import Optional
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image
from wagtail.images import get_image_model

# Configure logging
logger = logging.getLogger(__name__)

# Configuration with settings override support
ALLOWED_FORMATS = getattr(
    settings,
    'IMAGE_URL_UPLOAD_FORMATS',
    {"avif", "gif", "jpeg", "jpg", "png", "webp"}
)
MAX_FILE_SIZE = getattr(
    settings,
    'IMAGE_URL_UPLOAD_MAX_SIZE',
    10 * 1024 * 1024  # 10 MB
)
TIMEOUT = getattr(
    settings,
    'IMAGE_URL_UPLOAD_TIMEOUT',
    (5, 15)  # (connect, read)
)


def _is_private_address(hostname: str) -> bool:
    """
    Prevent SSRF by blocking private/loopback/reserved IPs.

    Args:
        hostname: The hostname to check

    Returns:
        True if the hostname resolves to a private/reserved IP address
    """
    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        # Hostname is not a direct IP, resolve it
        try:
            resolved = socket.gethostbyname(hostname)
            ip = ipaddress.ip_address(resolved)
        except (socket.gaierror, ValueError) as e:
            logger.warning(f"Failed to resolve hostname {hostname}: {e}")
            return True

    is_blocked = (
        ip.is_private or
        ip.is_loopback or
        ip.is_reserved or
        ip.is_multicast
    )

    if is_blocked:
        logger.warning(f"Blocked access to private/reserved IP: {ip}")

    return is_blocked


def validate_image_url(url: str) -> None:
    """
    Lightweight pre-check before downloading the whole file.

    Validates URL scheme, hostname, and performs a HEAD request
    to check the content type.

    Args:
        url: The URL to validate

    Raises:
        ValidationError: If the URL is invalid or unsafe
    """
    parsed = urlparse(url)

    # Validate URL scheme
    if parsed.scheme not in ("http", "https"):
        raise ValidationError("Only http/https URLs are allowed.")

    # Validate hostname exists and is not private
    if not parsed.hostname or _is_private_address(parsed.hostname):
        raise ValidationError(
            "Blocked for security reasons (private/loopback address)."
        )

    # Perform HEAD request to validate content type
    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=TIMEOUT,
            headers={'User-Agent': 'Wagtail-Image-From-URL/0.1.0'}
        )
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            raise ValidationError(
                f"URL does not point to an image (Content-Type: {content_type})."
            )
    except requests.RequestException as e:
        logger.error(f"Failed to validate URL {url}: {e}")
        raise ValidationError(f"Could not fetch image headers: {str(e)}")


def get_image_from_url(url: str, user=None, collection=None):
    """
    Download and create a Wagtail image from a URL.

    This function downloads an image from a URL, validates it,
    and creates a Wagtail Image object.

    Args:
        url: The URL of the image to download
        user: The user uploading the image (optional)
        collection: The collection to add the image to (optional)

    Returns:
        A Wagtail Image object

    Raises:
        ValidationError: If the URL is invalid, blocked, or the image is invalid
        requests.RequestException: If the download fails
    """
    parsed = urlparse(url)

    # Enforce SSRF safety
    if not parsed.hostname or _is_private_address(parsed.hostname):
        raise ValidationError(
            "Blocked for security reasons (private/loopback address)."
        )

    logger.info(f"Downloading image from URL: {url}")

    try:
        response = requests.get(
            url,
            stream=True,
            timeout=TIMEOUT,
            headers={'User-Agent': 'Wagtail-Image-From-URL/0.1.0'}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to download image from {url}: {e}")
        raise

    # Validate content type
    content_type = response.headers.get("Content-Type", "").lower()
    if not content_type.startswith("image/"):
        raise ValidationError(
            f"Invalid Content-Type: {content_type or 'missing'}"
        )

    # Download content in chunks to prevent memory issues
    content = b""
    try:
        for chunk in response.iter_content(1024 * 1024):  # 1MB chunks
            content += chunk
            if len(content) > MAX_FILE_SIZE:
                raise ValidationError(
                    f"Image too large (max {MAX_FILE_SIZE // (1024 * 1024)} MB)."
                )
    except requests.RequestException as e:
        logger.error(f"Failed to download image content: {e}")
        raise ValidationError(f"Download failed: {str(e)}")

    # Validate with Pillow
    try:
        img = Image.open(ContentFile(content))
        img.load()  # Actually load the image data
        fmt = img.format.lower() if img.format else None
    except Exception as e:
        logger.error(f"Failed to validate image: {e}")
        raise ValidationError("The file is not a valid image.")

    # Validate format
    if fmt not in ALLOWED_FORMATS:
        raise ValidationError(
            f"Unsupported format: {fmt.upper() if fmt else 'unknown'}. "
            f"Allowed: {', '.join(sorted(ALLOWED_FORMATS))}"
        )

    # Create Wagtail Image object
    ImageModel = get_image_model()
    filename = f"{uuid.uuid4().hex}.{fmt or 'jpg'}"

    # Generate a better title from the URL
    title = os.path.basename(parsed.path) or "Imported image"
    # Remove file extension from title if present
    title = os.path.splitext(title)[0] if '.' in title else title

    create_kwargs = {
        'title': title,
        'file': ContentFile(content, name=filename),
        'uploaded_by_user': user,
    }

    if collection:
        create_kwargs['collection'] = collection

    image = ImageModel.objects.create(**create_kwargs)
    logger.info(f"Successfully created image: {image.title} (ID: {image.id})")

    return image
