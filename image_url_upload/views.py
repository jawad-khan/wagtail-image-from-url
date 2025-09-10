from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext as _
from wagtail.admin import messages as wagtail_messages
from django.urls import reverse


from .forms import AddImageFromURLForm
from .utils import get_image_from_url


@staff_member_required
def add_image_via_url(request):
    
    breadcrumbs_items = [
        {'url': reverse('wagtailadmin_home'), 'label': _('Home')},
        {'url': reverse('wagtailimages:index'), 'label': _('Images')},
        {'url': reverse('wagtailimages:add_image_via_url'), 'label': _('Add image from URL')},
    ]

    if request.method == "POST":
        form = AddImageFromURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["image_url"]
            try:
                image = get_image_from_url(url, user=request.user)
                wagtail_messages.success(
                    request, f"Image '{image.title}' added successfully."
                )
                return redirect("wagtailimages:index")
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = AddImageFromURLForm()

    return render(
        request,
        "image_url_upload/add_via_url.html",
        {"form": form, "breadcrumbs_items": breadcrumbs_items},
    )
