from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from .views import AddImageViaURLView, CustomImageIndexView, AddFromURLView


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path(
            "images/add-url/",
            AddImageViaURLView.as_view(),
            name="add_image_via_url",
        ),
        path(
            "images/add_from_url/", AddFromURLView.as_view(), name="add_from_url"
        ),
    ]


@hooks.register("register_admin_urls")
def register_custom_image_index():
    return [
        path("images-w-url/", CustomImageIndexView.as_view(), name="images_w_url_index"),
    ]


@hooks.register("register_admin_menu_item")
def register_images_menu_item():
    return MenuItem(
        _("Images"),
        reverse("images_w_url_index"),
        name="custom_images",
        icon_name="image",
        order=301,
    )


@hooks.register("construct_main_menu")
def hide_default_images_menu_item(request, menu_items):
    # Remove the default "Images" menu item
    # Now the custom "Images" menu item registered above will be the only one
    # This ensures that the custom view is used when clicking on "Images"
    print("Menu items before filtering:", [item.name for item in menu_items])
    menu_items[:] = [item for item in menu_items if item.name != "images"]
    print("Menu items after filtering:", [item.name for item in menu_items])

    # from wagtail.admin.menu import MenuItem
    # from django.urls import reverse

    # menu_items.append(
    #     MenuItem("Images", reverse("wowindex"), icon_name="image", order=301)
    # )

    # print("Menu items after filtering:", [item.name for item in menu_items])
