from django import forms

class ImageUrlForm(forms.Form):
    image_url = forms.URLField(
        label="Image URL",
        required=True,
        widget=forms.URLInput(attrs={"placeholder": "Paste image URL here", "class": "form-control"}),
    )
