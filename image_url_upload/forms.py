from django import forms
import requests


class ImageURLForm(forms.Form):
    image_url = forms.URLField(
        label="Image URL",
        required=True,
        widget=forms.URLInput(attrs={
            "placeholder": "https://example.com/image.jpg",
            "class": "w-full border rounded p-2"
        }),
        help_text="Enter a direct link to an image (JPG, PNG, or GIF).",
    )

    def clean_image_url(self):
        image_url = self.cleaned_data["image_url"]
    
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            content_length = response.headers.get("Content-Length")
    
            if content_length and int(content_length) > self.MAX_FILE_SIZE_MB * 1024 * 1024:
                raise ValidationError(
                    f"File size exceeds {self.MAX_FILE_SIZE_MB} MB limit."
                )
        except requests.RequestException:
            raise ValidationError("Could not validate image URL.")
    
        return image_url
