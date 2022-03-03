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
    # split given request to single lines
    lst = request_str.split("\n")

    request_dict = {}

    # for each
    for line in lst:
        if line.strip() == "":
            continue

        temp = line.split(": ", 1)

        # append to dict
        request_dict[temp[0]] = temp[1]

    # print(request_dict)
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
    # os.path.join() won't work properly if elements start/end with /, hence .ctrip()
    if "index.html" in resource:
        resource_path = os.path.join(public_html, resource.strip("/"))

    else:
        resource_path = os.path.join(public_html, resource.strip("/"), "index.html")

    # does given path even lead to any existing object?
    # try:
    # get path to main directory and the requested file/dir
    full_path = os.path.join(os.getcwd(), resource_path)

    if os.path.exists(full_path):
        return resource_path

    else:
        raise Http404Exception(resource=resource)

    # except:  # find specific error!
    #     return "Path could not be found"


def read_resource(resource_path):
    """
    Read content of the resource (path in local filesystem) and return its content.

    path: str
    """

    path = Path(resource_path)

    with path.open("rt") as f:
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
        case _:
            raise Http500Exception()


def build_response_headers(resource_len):
    """
    Always include Keep-alive: Close
    Alawys include Server: http_serv
    Include Content-Length header
    """

    return f"Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: {resource_len}"
