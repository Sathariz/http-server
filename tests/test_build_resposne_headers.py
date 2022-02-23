from http_serv.server import build_resposne_headers

def test_build_resposne_headers_x():
    resrc_len = "x"

    expected = 'Keep-alive: Close\nServer: http_serv\nContent-Length: x'

    actual = build_resposne_headers(resrc_len)

    assert expected == actual

def test_build_resposne_headers_complex():
    resrc_len = "Mn+34Df6/78"

    expected = 'Keep-alive: Close\nServer: http_serv\nContent-Length: Mn+34Df6/78'

    actual = build_resposne_headers(resrc_len)

    assert expected == actual
