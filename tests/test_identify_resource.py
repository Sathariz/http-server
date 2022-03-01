from http_serv.server import identify_resource


def test_identify_resource_blog():
    public_html = "http_serv/public_html"
    resource = "/blog"

    expected = "http_serv/public_html/blog/index.html"

    actual = identify_resource(public_html, resource)

    assert expected == actual


def test_identify_resource_dash():
    public_html = "http_serv/public_html"
    resource = "/"

    expected = "http_serv/public_html/index.html"

    actual = identify_resource(public_html, resource)

    assert expected == actual


def test_identify_resource_index():
    public_html = "http_serv/public_html"
    resource = "/index.html"

    expected = "http_serv/public_html/index.html"

    actual = identify_resource(public_html, resource)

    assert expected == actual


def test_identify_resource_blog_index():
    public_html = "http_serv/public_html"
    resource = "/blog/index.html"

    expected = "http_serv/public_html/blog/index.html"

    actual = identify_resource(public_html, resource)

    assert expected == actual
