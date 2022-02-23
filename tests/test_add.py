from http_serv.server import add

def test_add():
    actual = add(2,5)
    expected = 7

    assert expected == actual
