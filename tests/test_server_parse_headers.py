from http_serv.server import parse_headers

def test_parse_headers():
    header_string = """Host: localhost:8080
User-Agent: HTTPie/2.6.0
Accept-Encoding: gzip, deflate"""
    expected = {
        'Host': 'localhost:8080',
        'User-Agent': 'HTTPie/2.6.0',
        'Accept-Encoding': 'gzip, deflate'
    }

    actual = parse_headers(header_string)

    assert actual == expected


def test_parse_headers_with_forwarder_for():
    header_string = """Host: localhost:8080
User-Agent: HTTPie/2.6.0
Accept-Encoding: gzip, deflate
X-Forwarded-For: asdf"""

    expected = {
        'Host': 'localhost:8080',
        'User-Agent': 'HTTPie/2.6.0',
        'Accept-Encoding': 'gzip, deflate',
        'X-Forwarded-For': 'asdf',
    }

    actual = parse_headers(header_string)

    assert actual == expected