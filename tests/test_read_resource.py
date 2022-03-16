import pytest
from http_serv.server import read_resource


@pytest.fixture
def folder_path():
    return 'public_html'


@pytest.mark.parametrize(
    ["file_path", "file_content"],
    [
        ("/index.html", "<h1>Index of public html</h1>"),
        ("/blog/index.html", "<h1>Blog</h1>"),
        ("/blog/note.txt", "Lorem ipsum")
    ]
)
def test_read_resource(file_path, file_content, folder_path):
    expected = (file_content, len(file_content))
    full_path = folder_path + file_path
    
    actual = read_resource(full_path)

    assert expected == actual
