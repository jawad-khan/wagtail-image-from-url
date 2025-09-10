# image_url_upload/views.py
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from wagtail.admin.views import generic
from wagtail.admin import messages as wagtail_messages

from .utils import get_image_from_url


class ImageURLForm(forms.Form):
    image_url = forms.URLField(label=_("Image URL"))


class AddImageViaURLView(generic.FormView):
    form_class = ImageURLForm
    template_name = "image_url_upload/add.html"
    page_title = _("Add image via URL")
    header_icon = "image"

    def form_valid(self, form):
        url = form.cleaned_data["image_url"]
        try:
            image = get_image_from_url(url, user=self.request.user)
            wagtail_messages.success(
                self.request, _("Image '%(title)s' added successfully.") % {"title": image.title}
            )
            return redirect("wagtailimages:index")
        except ValidationError as e:
            form.add_error("image_url", e.message)
            return self.form_invalid(form)

    def get_breadcrumbs(self):
        return [
            {"url": reverse("wagtailadmin_home"), "label": _("Home")},
            {"url": reverse("wagtailimages:index"), "label": _("Images")},
            {"url": "", "label": _("Add image via URL")},
        ]
