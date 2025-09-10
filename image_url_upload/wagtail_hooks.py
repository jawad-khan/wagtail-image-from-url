from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse
from . import views
from django.urls import path


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path(
            "images/add-url/",
            AddImageViaURLView.as_view(),
            name="add_image_via_url",
        ),
    ]

# Add menu item in Wagtail admin
@hooks.register("register_admin_menu_item")
def register_add_image_from_url_button():
    return MenuItem(
        label="Add image from URL",
        url=reverse("add_image_via_url"),
        order=1000  # adjust order as needed
    )
