import os
from pathlib import Path

from http_serv.http_status import HttpStatusCode
from http_serv.http_exceptions import Http404Exception, Http500Exception


def parse_first_line(first_line):
    """
    1. Split first line into verb, resource and protocol
    return as a dictionary
    e.g.: GET / HTTP/1.1
    {f"Error with {resource_path}"
        'verb': 'GET',
        'resource': '/',
        'protocol', 'HTTP/1.1'
    }
    """
    first_line.split()[0]
    dict = {
        "verb": first_line.split()[0],
        "resource": first_line.split()[1],
        "protocol": first_line.split()[2],
    }
    return dict


def parse_headers(request_str):
    """
    Read all headers (multiline) and parse them into dict.
    E.g.:
    Host: localhost:8080
    User-Agent: HTTPie/2.6.0
    Accept-Encoding: gzip, deflate
    returns
    {
        'Host': 'localhost:8080',
        'User-Agent': 'HTTPie/2.6.0',
        'Accept-Encoding': 'gzip, deflate'
    }
    """
    lst = request_str.split("\n")

    request_dict = {}

    for line in lst:
        if line.strip() == "":
            continue

        temp = line.split(": ", 1)

        request_dict[temp[0]] = temp[1]

    return request_dict


def identify_resource(public_html, resource):
    """
    Return path to file at specific resource. eg:
    '/index.html' -> public_html/index.html
    '/' -> public_html/index.html
    '/blog' -> public_html/blog/index.html
    '/blog/index.html' -> public_html/blog/index.html
    '/nonexisting' -> raise exception
    """
    # given that resource starts with /
    # os.path.join() won't work properly if elements start/end with /, hence .strip()
    if "." in resource:
        resource_path = os.path.join(public_html, resource.strip("/"))        
    else:
        resource_path = os.path.join(public_html, resource.strip("/"), "index.html")

    full_path = os.path.join(os.getcwd(), resource_path)

    if os.path.exists(full_path):
        if full_path.endswith(".html"):
            return (resource_path, "text/html")
        if full_path.endswith(".txt"):
            return (resource_path, "text/plain; charset=utf-8")
        elif full_path.endswith(".css"):
            return (resource_path, "text/css")
        elif full_path.endswith(".json"):
            return (resource_path, "application/json")
        elif full_path.endswith('.png'):
            return (resource_path, 'image/png')
        else:
            return (resource_path, "application/octet-stream")

    else:
        raise Http404Exception(resource=resource)



def read_resource(resource_path):
    """
    Read content of the resource (path in local filesystem) and return its content.
    path: str
    """

    path = Path(resource_path)

    # mode = 'rt'
    # if mime_type in {'application/octet-stream', 'image/png'}:
    #     mode = 'rb'


    with path.open('rb') as f:
        data = f.read()

    length = len(data)

    return data, length


def build_status_line(status_code):
    """
    For supported status codes build proper http status line
    eg:
    200 -> HTTP/1.1 200 OK
    404 -> HTTP/1.1 404 Not Found
    500 -> HTTP/1.1 500 Internal Server Error
    """

    match status_code:
        case HttpStatusCode.OK:
            return "HTTP/1.1 200 OK"
        case HttpStatusCode.NOT_FOUND:
            return "HTTP/1.1 404 Not Found"
        case HttpStatusCode.INTERNAL_SERVER_ERROR:
            return "HTTP/1.1 500 Internal Server Error"
        case HttpStatusCode.CREATED:
            return "HTTP/1.1 201 Created"
        case HttpStatusCode.NO_CONTENT:
            return "HTTP/1.1 204 No Content"
        case _:
            raise Http500Exception()


def build_response_headers(resource_len, mime):
    """
    Always include Keep-alive: Close
    Alawys include Server: http_serv
    Include Content-Length header
    """

    return f"Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: {resource_len}\r\nContent-type: {mime}"