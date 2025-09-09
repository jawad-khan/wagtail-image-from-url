 # wagtail/images/utils.py
import requests
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.core.exceptions import ValidationError
from wagtail.images import get_image_model

def get_image_from_url(url, title=None, user=None):
    """
    Download an image from a URL and save it to the Wagtail Image model.

    Args:
        url (str): Image URL.
        title (str, optional): Title for the image.
        user (User, optional): User who is uploading.

    Returns:
        Image: The created Wagtail Image instance.
    """
    Image = get_image_model()

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise ValidationError(f"Could not fetch image: {e}")

    # Ensure it looks like an image
    content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        raise ValidationError("The provided URL does not point to a valid image.")

    # Save to Wagtail's Image model
    file_ext = content_type.split("/")[-1]
    filename = f"downloaded.{file_ext}"

    image_file = ContentFile(response.content, name=filename)

    image = Image(title=title or filename, file=image_file)
    if user:
        image.uploaded_by_user = user
    image.save()

    return image
