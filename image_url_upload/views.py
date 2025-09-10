# image_url_upload/views.py
import requests
from django import forms
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from wagtail.admin.views import generic
from wagtail.images import get_image_model


MAX_FILE_SIZE_MB = 5
ImageModel = get_image_model()


class ImageURLForm(forms.ModelForm):
    image_url = forms.URLField(label=_("Image URL"))

    class Meta:
        model = ImageModel
        fields = []  # we only use our custom URL field

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


class AddImageViaURLView(generic.CreateView):
    """
    Wagtail admin view for adding images via URL.
    """

    form_class = ImageURLForm
    template_name = "image_url_upload/add.html"
    page_title = _("Add image via URL")
    header_icon = "image"
    model = ImageModel

    def form_valid(self, form):
        url = form.cleaned_data["image_url"]
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        file_name = url.split("/")[-1] or "imported.jpg"
        image_file = ContentFile(response.content, name=file_name)

        self.object = self.model.objects.create(
            title=file_name,
            file=image_file,
            uploaded_by_user=self.request.user,
        )

        return redirect("wagtailimages:index")

    def get_breadcrumbs(self):
        """
        Override breadcrumbs to show:
        Home → Images → Add image via URL
        """
        return [
            {"url": reverse("wagtailadmin_home"), "label": _("Home")},
            {"url": reverse("wagtailimages:index"), "label": _("Images")},
            {"url": "", "label": _("Add image via URL")},
        ]
