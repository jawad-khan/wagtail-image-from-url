from django import forms
from django.utils.translation import gettext_lazy as _


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
