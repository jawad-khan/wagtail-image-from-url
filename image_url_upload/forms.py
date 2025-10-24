"""
Forms for image URL upload functionality.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ImageURLForm(forms.Form):
    """
    Form for validating and processing image URLs.

    This form performs basic validation on image URLs before
    they are processed by the backend.
    """

    image_url = forms.URLField(
        label=_("Image URL"),
        required=True,
        widget=forms.URLInput(
            attrs={
                "placeholder": "https://example.com/image.jpg",
                "class": "w-field__input",
            }
        ),
        help_text=_(
            "Enter a direct link to an image (AVIF, JPG, JPEG, PNG, GIF, WEBP)."
        ),
    )

    def clean_image_url(self):
        """
        Validate that the URL uses HTTP or HTTPS protocol.

        Returns:
            str: The cleaned URL

        Raises:
            ValidationError: If the URL scheme is not http or https
        """
        image_url = self.cleaned_data["image_url"]

        if not image_url.lower().startswith(("http://", "https://")):
            raise ValidationError(
                _("Only http/https URLs are allowed."), code="invalid_scheme"
            )

        return image_url
