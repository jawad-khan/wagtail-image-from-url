# image_url_upload/wagtail_hooks.py

from django.urls import path
from wagtail import hooks
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from django.urls import reverse

from .views import AddImageViaURLView  # ✅ import your view!


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path(
            "images/add-url/",
            AddImageViaURLView.as_view(),
            name="add_image_via_url",
        ),
    ]


@hooks.register("register_admin_menu_item")
def register_admin_menu_item():
    return MenuItem(
        _("Add image via URL"),
        reverse("add_image_via_url"),
        icon_name="image",
        order=201,
    )
