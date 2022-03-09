from http_serv.server import read_resource


def test_read_resource_index():
    path = "public_html/index.html"

    expected = ("<h1>Index of public html</h1>", 29)

    actual = read_resource(path)

    assert expected == actual


def test_read_resource_blog_index():
    path = "public_html/blog/index.html"

    expected = ("<h1>Blog</h1>", 13)

    actual = read_resource(path)

    assert expected == actual


# def test_read_resource_blog_index():
#     resource = "http localhost:8080 blog/index.html"

#     expected = "blog/index.html"
#     actual = read_resource(resource)

#     assert expected == actual


# def test_read_resource_blog():
#     resource = "http localhost:8080 blog"

#     expected = "blog"
#     actual = read_resource(resource)

#     assert expected == actual


# def test_read_resource_index():
#     resource = "http localhost:8080 index.html"

#     expected = "index.html"
#     actual = read_resource(resource)

#     assert expected == actual


# def test_read_resource_blog_slash():
#     resource = "http localhost:8080 /"

#     expected = "/"
#     actual = read_resource(resource)

#     assert expected == actual
