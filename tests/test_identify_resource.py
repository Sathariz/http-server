import pytest

from http_serv.server import identify_resource
from http_serv.http_exceptions import Http404Exception, Http500Exception
from http_serv.utils import build_response_headers


@pytest.fixture()
def public_html():
    return "public_html"


@pytest.mark.parametrize(
    ["resource", "mime_type", "file_path"],
    [
        ("/blog", "text/html", "/blog/index.html"),
        ("/", "text/html", "/index.html"),
        ("/simple-data.json", "application/json", "/simple-data.json"),
        ("/blog/style.css", "text/css", "/blog/style.css"),
        ("/blog/note.txt", "text/plain; charset=utf-8", "/blog/note.txt"),
    ],
)
def test_identify_resource(resource, mime_type, file_path, public_html):
    actual = identify_resource(public_html, resource)
    full_path = public_html + file_path

    assert (full_path, mime_type) == actual


def test_identify_resource_parrot(public_html):
    resource = "/parrot.png"

    expected = (f"{public_html}/parrot.png", "image/png")

    actual = identify_resource(public_html, resource)

    assert expected == actual


def test_rasises_404(public_html):
    resource = "non-existing.xyz"

    with pytest.raises(Http404Exception):
        identify_resource(public_html, resource)
