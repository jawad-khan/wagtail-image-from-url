from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import requests

class AddImageFromURLForm(forms.Form):
    image_url = forms.URLField(
        label=_("Image URL"),
        required=True,
        widget=forms.URLInput(attrs={
            "placeholder": _("https://example.com/image.jpg"),
            "class": "w-input"
        }),
        help_text=_("Enter a direct link to an image.")
    )

    MAX_FILE_SIZE_MB = 10  # ✅ constraint (adjust as needed)

    def clean_image_url(self):
        url = self.cleaned_data["image_url"]

        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            content_length = response.headers.get("Content-Length")

            if content_length and int(content_length) > self.MAX_FILE_SIZE_MB * 1024 * 1024:
                raise ValidationError(
                    f"File size exceeds {self.MAX_FILE_SIZE_MB} MB limit."
                )
        except requests.RequestException:
            raise ValidationError("Could not validate image URL.")

        return url
