import pytest
from django.urls import reverse
from django.test import RequestFactory
from image_url_upload.views import AddImageViaURLView

@pytest.mark.django_db
def test_add_image_via_url_view_get():
    factory = RequestFactory()
    request = factory.get(reverse("add_image_via_url"))
    response = AddImageViaURLView.as_view()(request)
    assert response.status_code == 200
