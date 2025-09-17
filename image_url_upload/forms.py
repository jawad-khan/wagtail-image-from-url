from django import forms
from django.core.exceptions import ValidationError


class ImageURLForm(forms.Form):
    MAX_FILE_SIZE_MB = 10  # 10 MB

    image_url = forms.URLField(
        label="Image URL",
        required=True,
        widget=forms.URLInput(
            attrs={"placeholder": "https://example.com/image.jpg", "class": "w-full border rounded p-2"}
        ),
        help_text="Enter a direct link to an image (AVIF, JPG, JPEG, PNG, GIF, WEBP).",
    )

    def clean_image_url(self):
        image_url = self.cleaned_data["image_url"]
        # ✅ Only basic URL + scheme validation here
        if not image_url.lower().startswith(("http://", "https://")):
            raise ValidationError("Only http/https URLs are allowed.")

        return image_url
