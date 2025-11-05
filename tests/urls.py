"""
URL configuration for tests.
"""
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from image_url_upload import views

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # Image URL upload views
    path("images/add_from_url/", views.AddFromURLView.as_view(), name="add_from_url"),
    path("images-w-url/", views.CustomImageIndexView.as_view(), name="images_w_url_index"),
    # Wagtail core URLs
    path("", include(wagtail_urls)),
]

