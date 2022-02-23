from http_serv.server import parse_first_line


def test_parse_first_line():
    #AAA
    # Arrange

    line = "GET / HTTP/1.1"
    expected = {
        'verb': 'GET',
        'resource': '/',
        'protocol': 'HTTP/1.1'
    }

    # act

    actual = parse_first_line(line)

    # asssert

    assert actual == expected

def test_parse_first_line_post():
    line = "POST / HTTP/1.1"
    expected = {
        'verb': 'POST',
        'resource': '/',
        'protocol': 'HTTP/1.1'
    }
    actual = parse_first_line(line)
    assert actual == expected

def test_parse_first_line_head():
    line = "HEAD / HTTP/1.1"
    expected = {
        'verb': 'HEAD',
        'resource': '/',
        'protocol': 'HTTP/1.1'
    }
    actual = parse_first_line(line)
    assert actual == expected

def test_parse_first_line_index():
    line = "GET /index.html HTTP/1.1"
    expected = {
        'verb': 'GET',
        'resource': '/index.html',
        'protocol': 'HTTP/1.1'
    }
    actual = parse_first_line(line)
    assert actual == expected

def test_parse_first_line_image():
    line = "GET /image.png HTTP/1.1"
    expected = {
        'verb': 'GET',
        'resource': '/image.png',
        'protocol': 'HTTP/1.1'
    }
    actual = parse_first_line(line)
    assert actual == expected


def test_parse_first_video():
    line = "GET /videos/video.mkv HTTP/1.1"
    expected = {
        'verb': 'GET',
        'resource': '/videos/video.mkv',
        'protocol': 'HTTP/1.1'
    }
    actual = parse_first_line(line)
    assert actual == expected