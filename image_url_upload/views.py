from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import FormView
from wagtail import hooks
from wagtail.admin import messages as wagtail_messages
from wagtail.admin.widgets.button import HeaderButton
from wagtail.images.views.images import IndexView as ImageIndexView

from .forms import ImageURLForm
from .utils import get_image_from_url


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
            return redirect("images_w_url_index")

        # create Wagtail Image
        wagtail_messages.success(self.request, f"Image '{image.title}' added successfully!")

        return redirect("images_w_url_index")


class CustomImageIndexView(ImageIndexView):
    @property
    def header_buttons(self):
        print(hooks.get_hooks("register_admin_menu_item"))
        # Start with the default buttons from IndexView
        buttons = super().header_buttons

        # Add a custom button
        buttons.append(
            HeaderButton(
                label="Add an Image from URL",
                url=reverse("add_image_via_url"),
                icon_name="plus",
            )
        )

        return buttons
