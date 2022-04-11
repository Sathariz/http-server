import pytest
from http_serv.server import build_response_headers


@pytest.mark.parametrize(
    ["resource_len", "mime_type"],
    [
        ("x", "text/css"),
        ("123", "text/plain"),
        ("42", "text/html"),
        ("20", "application/json"),
        ("100", "application/octet-stream"),
    ],
)
def test_build_response_headers(resource_len, mime_type):
    actual = build_response_headers(resource_len, mime_type)
    expected = f"Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: {resource_len}\r\nContent-type: {mime_type}"

    assert expected == actual
