import pytest
from image_url_upload.forms import ImageURLForm


def test_image_url_form_valid():
    form = ImageURLForm(data={"image_url": "https://example.com/image.jpg"})
    assert form.is_valid()


def test_image_url_form_invalid_scheme():
    form = ImageURLForm(data={"image_url": "ftp://example.com/image.jpg"})
    assert not form.is_valid()
    assert "Only http/https URLs are allowed." in form.errors["image_url"][0]


def test_image_url_form_invalid_url():
    form = ImageURLForm(data={"image_url": "not-a-url"})
    assert not form.is_valid()
