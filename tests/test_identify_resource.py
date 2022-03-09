import pytest

from http_serv.server import identify_resource
from http_serv.http_exceptions import Http404Exception, Http500Exception


@pytest.fixture()
def public_html():
    return 'public_html'

def test_identify_resource_blog_html(public_html):
    resource = "/blog"

    expected = (f"{public_html}/blog/index.html", "text/html")

    actual = identify_resource(public_html, resource)

    assert expected == actual

def test_identify_resource_parrot(public_html):
    resource = "/parrot.png"

    expected = (f"{public_html}/parrot.png", "application/octet-stream")

    actual = identify_resource(public_html, resource)

    assert expected == actual

def test_rasises_404(public_html):
    resource = 'non-existing.xyz'

    with pytest.raises(Http404Exception):
        identify_resource(public_html, resource)

# def test_identify_resource_dash_html():
#     public_html = "http_serv/public_html"
#     resource = "/"

#     expected = ("http_serv/public_html/index.html", "text/html")

#     actual = identify_resource(public_html, resource)

#     assert expected == actual


# def test_identify_resource_json():
#     public_html = "http_serv/public_html"
#     resource = "/simple-data.json"

#     expected = ("http_serv/public_html/simple-data.json", "application/json")

#     actual = identify_resource(public_html, resource)

#     assert expected == actual


# def test_identify_resource_blog_index_html():
#     public_html = "http_serv/public_html"
#     resource = "/blog/index.html"

#     expected = ("http_serv/public_html/blog/index.html", "text/html")

#     actual = identify_resource(public_html, resource)

#     assert expected == actual


# def test_identify_resource_blog_css():
#     public_html = "http_serv/public_html"
#     resource = "/blog/style.css"

#     expected = ("http_serv/public_html/blog/style.css", "text/css")

#     actual = identify_resource(public_html, resource)

#     assert expected == actual


# def test_identify_resource_blog_other():
#     public_html = "http_serv/public_html"
#     resource = "/blog/note.txt"

#     expected = ("http_serv/public_html/blog/note.txt", "application/octet-stream")

#     actual = identify_resource(public_html, resource)

#     assert expected == actual
