from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import FormView
from wagtail import hooks
from wagtail.admin import messages as wagtail_messages
from wagtail.admin.widgets.button import HeaderButton
from wagtail.images.views.images import IndexView as ImageIndexView
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
from wagtail.images.views.multiple import AddView
import os

import requests
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


class AddFromURLView(AddView):
    # We inherit template_name, permission_policy, etc. from AddView

    def post(self, request):
        image_url = request.POST.get("url")
        if not image_url:
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "Please provide a URL.",
                }
            )

        try:
            # 1. Download the image data
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            # 2. Wrap the downloaded content in a Django-friendly file object
            # This is the key step to making it compatible with the existing form.
            file = SimpleUploadedFile(
                name=os.path.basename(image_url.split("?")[0]),
                content=response.content,
                content_type=response.headers.get("Content-Type"),
            )

            # 3. Use the inherited form to validate the file
            upload_form_class = self.get_upload_form_class()
            form = upload_form_class(
                {"title": file.name, "collection": request.POST.get("collection", 1)},
                {"file": file},
                user=request.user,
            )

            if form.is_valid():
                # 4. Save the object using the inherited save method
                self.object = self.save_object(form)

                # 5. Return the JSON response using the inherited method.
                # This method already handles duplicate checking!
                return JsonResponse(self.get_edit_object_response_data())
            else:
                # Reuse the generic invalid response logic
                print("\n\n\n\n\n\n\n")
                print(form.errors)
                print("\n\n\n\n\n\n\n")
                return JsonResponse(self.get_invalid_response_data(form))

        except requests.exceptions.RequestException as e:
            # Handle download errors
            return JsonResponse(
                {
                    "success": False,
                    "error_message": f"Download failed: {str(e)}",
                }
            )
