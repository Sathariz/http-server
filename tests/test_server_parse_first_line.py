import pytest
from http_serv.server import parse_first_line


@pytest.mark.parametrize(
    ["method", "resource"],
    [
        ("GET", "/"),
        ("POST", "/"),
        ("HEAD", "/"),
        ("GET", "/index.html"),
        ("GET", "/note.txt"),
        ("POST", "/abc.xyz"),
    ],
)
def test_parse_first_line(method, resource):
    line = method + " " + resource + " HTTP/1.1"
    expected = {"verb": f"{method}", "resource": f"{resource}", "protocol": "HTTP/1.1"}

    actual = parse_first_line(line)
