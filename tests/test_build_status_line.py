from http_serv.server import build_status_line

def test_build_status_line_404():
    code = "404"

    expected = "HTTP/1.1 404 Not Found"
    actual = build_status_line(code)

    assert expected == actual

def test_build_status_line_200():
    code = "200"

    expected = "HTTP/1.1 200 OK"
    actual = build_status_line(code)

    assert expected == actual


def test_build_status_line_500():
    code = "500"

    expected = "HTTP/1.1 500 Internal Server Error"
    actual = build_status_line(code)

    assert expected == actual


def test_build_status_line_error():
    code = "123"

    expected = f"Error code '{code}' not found."
    actual = build_status_line(code)

    assert expected == actual
