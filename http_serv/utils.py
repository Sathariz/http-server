import os
from pathlib import Path
import base64
from re import T

from pyparsing import html_comment

from http_serv.http_status import HttpStatusCode
from http_serv.http_exceptions import Http404Exception, Http500Exception, Http405Exception


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
    dct = {
        "verb": first_line.split()[0],
        "resource": first_line.split()[1],
        "protocol": first_line.split()[2],
    }
    return dct


def identify_request_method(method):
    if method == "GET" or method == "HEAD" or method == "POST":
        return method

    else:
        raise Http405Exception(method=method)

# def read_credentials(headers)

def is_auth_required(resource):
    auth_required = 'secret' in resource
    return auth_required

def authorized(headers):
    if 'Authorization' not in headers:
        return False

    encoded = headers['Authorization'].split()[1]    
    decoded = base64.b64decode(encoded)

    return decoded == b'john:doe'


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
    if public_html != "":
        if "." in resource:
            resource_path = os.path.join(public_html, resource.strip("/"))        
        else:
            resource_path = os.path.join(public_html, resource.strip("/"), "index.html")
        
        full_path = os.path.join(os.getcwd(), resource_path)
    
    else:
        full_path = resource.strip() #can be together?
        resource_path = resource.strip()


    if os.path.exists(full_path):
        if full_path.endswith(".html"):
            return (resource_path, "text/html")
        elif full_path.endswith(".txt"):
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


def read_resource(resource_path, method):
    """
    Read content of the resource (path in local filesystem) and return its content.
    path: str
    """

    path = Path(resource_path)

    with path.open('rb') as f:
        data = f.read()

    length = len(data)

    if method == "GET":
        return data, length

    else:
        return length


def save_resource(resource_path):
    """
        This method supports only files and requires file's exact path
    """
    file_path = Path(resource_path) # any need for that? do test

    #no need to check if path exists because it's already checked in identify_resource method
    file_name = os.path.basename(file_path)

    with file_path.open("rb") as i_file:
        with open(f"public_html/added_via_POST/{file_name}", "wb") as new_file:
            new_file.write(i_file.read())

    # it cuts off the sentence - dig into binary pls
    return f"The file {file_name} has been created.".encode()

    # todo:
    # handling duplicates and checking if file already exists

#works
def check_for_index_html(dir_path):
    
    if "index.html" not in dir_path and "." not in dir_path:
        full_path = os.path.join("public_html", dir_path.strip("/"), "index.html")

        if not os.path.exists(full_path):
            return True



def index_list_generator(current_dir_path):
    # HARDCODED!!!
    dir_path = os.path.join("public_html", current_dir_path.strip("/"))
    
    # give it nice formatting  style='margin-left:90px;
    html_code = "<center><table><tr><th>File Name</th><th>Link</th><th>Path</th></tr>"

    for f in os.scandir(dir_path):
        file_name = f.name
        html_code += f"<tr><td>{file_name}</td><td><a href='{os.path.join(dir_path, file_name)}' target=_blank>{file_name.split('.')[0]}</a></td><td>{os.path.join(dir_path, file_name)}</td></tr>"
    html_code += "</table></center>"

    html_code = html_code.encode() #??

    return html_code


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
        case HttpStatusCode.METHOD_NOT_ALLOWED:
            return "HTTP/1.1 405 Method Not Allowed"
        case HttpStatusCode.FORBIDDEN:
            return "HTTP/1.1 403 Forbidden"
        case HttpStatusCode.UNAUTHORIZED:
            return "HTTP/1.1 401 Unauthorized"
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