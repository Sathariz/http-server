from http_serv.server import build_response_headers


def test_build_resposne_headers_x_css():
    resrc_len = "x"
    mime_typ = "text/css"

    expected = "Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: x\r\nContent-type: text/css"

    actual = build_response_headers(resrc_len, mime_typ)

    assert expected == actual


def test_build_resposne_headers_complex_css():
    resrc_len = "Mn+34Df6/78"
    mime_typ = "text/css"

    expected = "Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: Mn+34Df6/78\r\nContent-type: text/css"

    actual = build_response_headers(resrc_len, mime_typ)

    assert expected == actual


def test_build_resposne_headers_complex_html():
    resrc_len = "Mn+34Df6/78"
    mime_typ = "text/html"

    expected = "Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: Mn+34Df6/78\r\nContent-type: text/html"

    actual = build_response_headers(resrc_len, mime_typ)

    assert expected == actual


def test_build_resposne_headers_y_json():
    resrc_len = "y"
    mime_typ = "application/json"

    expected = "Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: y\r\nContent-type: application/json"

    actual = build_response_headers(resrc_len, mime_typ)

    assert expected == actual


def test_build_resposne_headers_y_other():
    resrc_len = "y"
    mime_typ = "application/octet-stream"

    expected = "Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: y\r\nContent-type: application/octet-stream"

    actual = build_response_headers(resrc_len, mime_typ)

    assert expected == actual
