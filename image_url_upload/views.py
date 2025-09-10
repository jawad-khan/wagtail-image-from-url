import requests
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib import messages
from django.core.files.base import ContentFile

from wagtail.images.models import Image
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin import messages as wagtail_messages

from .forms import ImageURLForm
from .utils import validate_image_url, get_image_from_url


class AddImageViaURLView(FormView):
    template_name = "image_url_upload/add_via_url.html"
    form_class = ImageURLForm

    def form_valid(self, form):
        url = form.cleaned_data["image_url"]

        # # validate and fetch
        # if not validate_image_url(url):
        #     messages.error(self.request, "Invalid or unsupported image URL.")
        #     return redirect("wagtailimages:index")

        try:
            image = get_image_from_url(url, user=self.request.user)
        except Exception as e:
            messages.error(self.request, f"Failed to fetch image: {e}")
            return redirect("wagtailimages:index")

        # create Wagtail Image
        wagtail_messages.success(self.request, f"Image '{image.title}' added successfully!")

        return redirect("wagtailimages:index")
