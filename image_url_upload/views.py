# image_url_upload/views.py

import requests
from django import forms
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from wagtail.admin.views.generic import CreateView
from wagtail.images import get_image_model
from wagtail.images.views.images import AddView

MAX_FILE_SIZE_MB = 5


class ImageURLForm(forms.Form):
    image_url = forms.URLField(label=_("Image URL"))

    def clean_image_url(self):
        url = self.cleaned_data["image_url"]

        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            content_length = response.headers.get("Content-Length")

            if content_length and int(content_length) > MAX_FILE_SIZE_MB * 1024 * 1024:
                raise ValidationError(
                    _(f"File size exceeds {MAX_FILE_SIZE_MB} MB limit.")
                )
        except requests.RequestException:
            raise ValidationError(_("Could not validate image URL."))

        return url


class AddImageViaURLView(AddView):
    """
    A view similar to Wagtail's AddView, but fetches the image from a URL instead of file upload.
    """

    form_class = ImageURLForm
    template_name = "image_url_upload/add.html"
    model = get_image_model()

    def form_valid(self, form):
        url = form.cleaned_data["image_url"]
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        file_name = url.split("/")[-1]
        image_file = ContentFile(response.content, name=file_name)

        self.object = self.model.objects.create(
            title=file_name,
            file=image_file,
        )

        return redirect("wagtailimages:index")
