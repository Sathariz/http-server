from http_serv.server import build_response_headers


def test_build_resposne_headers_x():
    resrc_len = "x"

    expected = "Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: x"

    actual = build_response_headers(resrc_len)

    assert expected == actual


def test_build_resposne_headers_complex():
    resrc_len = "Mn+34Df6/78"

    expected = "Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: Mn+34Df6/78"

    actual = build_response_headers(resrc_len)

    assert expected == actual
