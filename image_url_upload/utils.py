import imghdr
import requests
from django.core.exceptions import ValidationError

# Allowed extensions & MIME types
ALLOWED_FORMATS = {"avif", "gif", "jpeg", "jpg", "png", "webp"}
MAX_FILE_SIZE_MB = 10

# Blocked private/reserved IPs (SSRF protection)
BLOCKED_IP_RANGES = [
    "127.", "10.", "172.", "192.168.", "169.254.", "::1"
]


def is_private_url(url: str) -> bool:
    """Basic check to block requests to local/private addresses."""
    return any(url.startswith(f"http://{prefix}") or url.startswith(f"https://{prefix}")
               for prefix in BLOCKED_IP_RANGES)


def validate_image_url(url: str) -> None:
    """Validate URL format, size, and type before downloading."""
    if is_private_url(url):
        raise ValidationError("Blocked request to private/internal address (possible SSRF).")

    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get("Content-Type", "")
        content_length = response.headers.get("Content-Length")

        # Size check
        if content_length and int(content_length) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"Image exceeds {MAX_FILE_SIZE_MB} MB limit.")

        # Format check
        if not any(fmt in content_type.lower() for fmt in ALLOWED_FORMATS):
            raise ValidationError("Unsupported image format. Allowed: AVIF, GIF, JPG, JPEG, PNG, WEBP.")

    except requests.RequestException:
        raise ValidationError("Could not validate image URL.")


def get_image_from_url(url: str, user=None):
    """Download image and save into Wagtail images collection."""
    import io
    from django.core.files.base import ContentFile
    from wagtail.images import get_image_model

    validate_image_url(url)

    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()

    # Confirm file signature
    raw_data = response.content
    image_type = imghdr.what(None, h=raw_data)
    if image_type not in ALLOWED_FORMATS:
        raise ValidationError("Downloaded file is not a valid supported image.")

    # Save into Wagtail Image model
    Image = get_image_model()
    filename = url.split("/")[-1]
    image_file = ContentFile(raw_data, name=filename)

    image = Image.objects.create(title=filename, file=image_file)
    if user:
        image.uploaded_by_user = user
        image.save()

    return image
