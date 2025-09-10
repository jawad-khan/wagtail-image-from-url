from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from wagtail.admin import messages as wagtail_messages

from .forms import ImageUrlForm
from .utils import get_image_from_url   # ✅ import the util function


@staff_member_required
def add_image_via_url(request):
     breadcrumbs_items = [
        BreadcrumbItem(_('Images'), url='wagtailimages:index'),
        BreadcrumbItem(_('Add image from URL')),
    ]


    if request.method == "POST":
        form = ImageUrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["image_url"]
            try:
                # ✅ actually save the image here
                image = get_image_from_url(url, user=request.user)

                wagtail_messages.success(
                    request, f"Image '{image.title}' added successfully."
                )
                return redirect("wagtailimages:index")
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = ImageUrlForm()

    return render(request, "image_url_upload/add_via_url.html", {"form": form, "breadcrumbs_items": breadcrumbs_items})
