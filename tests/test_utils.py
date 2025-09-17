import pytest
from django.core.exceptions import ValidationError
from image_url_upload.utils import validate_image_url, _is_private_address


def test_validate_image_url_valid(monkeypatch):
    class DummyResponse:
        headers = {"Content-Type": "image/jpeg"}
    monkeypatch.setattr("requests.head", lambda *a, **k: DummyResponse())
    validate_image_url("https://example.com/image.jpg")


def test_validate_image_url_invalid_scheme():
    with pytest.raises(ValidationError):
        validate_image_url("ftp://example.com/image.jpg")


def test_validate_image_url_private(monkeypatch):
    with pytest.raises(ValidationError):
        validate_image_url("http://127.0.0.1/image.jpg")


def test_is_private_address_loopback():
    assert _is_private_address("127.0.0.1")
    assert _is_private_address("localhost")


def test_validate_image_url_non_image_content_type(monkeypatch):
    class DummyResponse:
        headers = {"Content-Type": "text/html"}
    monkeypatch.setattr("requests.head", lambda *a, **k: DummyResponse())
    with pytest.raises(ValidationError, match="URL does not point to an image."):
        validate_image_url("https://example.com/notimage")


def test_validate_image_url_request_exception(monkeypatch):
    import requests
    def raise_exc(*a, **k):
        raise requests.RequestException("fail")
    monkeypatch.setattr("requests.head", raise_exc)
    with pytest.raises(ValidationError, match="Could not fetch image headers."):
        validate_image_url("https://example.com/image.jpg")


def test_get_image_from_url_ssrf(monkeypatch):
    from image_url_upload import utils
    with pytest.raises(ValidationError, match="Blocked for security reasons"):
        utils.get_image_from_url("http://127.0.0.1/image.jpg")


def test_get_image_from_url_invalid_content_type(monkeypatch):
    from image_url_upload import utils
    class DummyResponse:
        headers = {"Content-Type": "text/html"}
        def raise_for_status(self): pass
        def iter_content(self, n): return [b"fake"]
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResponse())
    with pytest.raises(ValidationError, match="Invalid Content-Type"):
        utils.get_image_from_url("https://example.com/notimage.jpg")


def test_get_image_from_url_large_file(monkeypatch):
    from image_url_upload import utils
    class DummyResponse:
        headers = {"Content-Type": "image/jpeg"}
        def raise_for_status(self): pass
        def iter_content(self, n): return [b"a" * (utils.MAX_FILE_SIZE + 1)]
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResponse())
    with pytest.raises(ValidationError, match="Image too large"):
        utils.get_image_from_url("https://example.com/large.jpg")


def test_get_image_from_url_pillow_error(monkeypatch):
    from image_url_upload import utils
    class DummyResponse:
        headers = {"Content-Type": "image/jpeg"}
        def raise_for_status(self): pass
        def iter_content(self, n): return [b"notanimage"]
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResponse())
    monkeypatch.setattr("PIL.Image.open", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    with pytest.raises(ValidationError, match="not a valid image"):
        utils.get_image_from_url("https://example.com/bad.jpg")


def test_get_image_from_url_unsupported_format(monkeypatch):
    from image_url_upload import utils
    class DummyImg:
        def load(self): pass
        format = "tiff"
    class DummyResponse:
        headers = {"Content-Type": "image/tiff"}
        def raise_for_status(self): pass
        def iter_content(self, n): return [b"fake"]
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResponse())
    monkeypatch.setattr("PIL.Image.open", lambda *a, **k: DummyImg())
    with pytest.raises(ValidationError, match="Unsupported format"):
        utils.get_image_from_url("https://example.com/file.tiff")
