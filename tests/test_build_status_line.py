import pytest

from http_serv.server import build_status_line
from http_serv.http_status import HttpStatusCode


@pytest.mark.parametrize(
    ["code", "status_line"],  # parameter names
    [  # list of parameter values
        (HttpStatusCode.OK, "HTTP/1.1 200 OK"),
        (HttpStatusCode.INTERNAL_SERVER_ERROR, "HTTP/1.1 500 Internal Server Error"),
        (HttpStatusCode.NO_CONTENT, "HTTP/1.1 204 No Content"),
        (HttpStatusCode.CREATED, "HTTP/1.1 201 Created"),
        (HttpStatusCode.NOT_FOUND, "HTTP/1.1 404 Not Found"),
    ],
)
def test_build_status_line(code, status_line):
    actual = build_status_line(code)

    assert status_line == actual
