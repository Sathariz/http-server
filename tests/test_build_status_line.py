import pytest

from http_serv.server import build_status_line
from http_serv.http_status import HttpStatusCode


def test_build_status_line_404():
    code = HttpStatusCode.NOT_FOUND

    expected = "HTTP/1.1 404 Not Found"
    actual = build_status_line(code)

    assert expected == actual


def test_build_status_line_200():
    code = HttpStatusCode.OK

    expected = "HTTP/1.1 200 OK"
    actual = build_status_line(code)

    assert expected == actual


def test_build_status_line_500():
    code = HttpStatusCode.INTERNAL_SERVER_ERROR

    expected = "HTTP/1.1 500 Internal Server Error"
    actual = build_status_line(code)

    assert expected == actual


@pytest.mark.skip(reason="Still working on http codes")
def test_build_status_line_error():
    code = HttpStatusCode.ASDF

    expected = f"Error code '{code}' not found."
    actual = build_status_line(code)

    assert expected == actual
