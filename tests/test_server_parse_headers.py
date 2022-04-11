from http_serv.server import parse_headers
import pytest


@pytest.mark.parametrize(
    ["header_string", "after_split"],
    [
        (
            """Host: localhost:8080
User-Agent: HTTPie/2.6.0
Accept-Encoding: gzip, deflate""",
            {
                "Host": "localhost:8080",
                "User-Agent": "HTTPie/2.6.0",
                "Accept-Encoding": "gzip, deflate",
            },
        ),
        (
            """Host: localhost:8080
User-Agent: HTTPie/2.6.0
Accept-Encoding: gzip, deflate
X-Forwarded-For: asdf""",
            {
                "Host": "localhost:8080",
                "User-Agent": "HTTPie/2.6.0",
                "Accept-Encoding": "gzip, deflate",
                "X-Forwarded-For": "asdf",
            },
        ),
    ],
)
def test_server_parse_headers(header_string, after_split):
    actual = parse_headers(header_string)

    assert after_split == actual
