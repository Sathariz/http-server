import socketserver, os
from pathlib import Path


def parse_first_line(first_line):
    """
    1. Split first line into verb, resource and protocol
    return as a dictionary
    e.g.: GET / HTTP/1.1
    {
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
        if line.strip() == '':
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
    try:
        # get path to main directory and the requested file/dir
        full_path = os.path.join(os.getcwd(), resource_path)

        if os.path.exists(full_path):
            return resource_path

        else:
            return f"Error with {resource_path}"

    except:  # find specific error!
        return "Path could not be found"


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

    if status_code == "200":
        # print("HTTP/1.1 200 OK")
        return "HTTP/1.1 200 OK"

    elif status_code == "404":
        # print("HTTP/1.1 404 Not Found")
        return "HTTP/1.1 404 Not Found"

    elif status_code == "500":
        # print("HTTP/1.1 500 Internal Server Error")
        return "HTTP/1.1 500 Internal Server Error"

    else:
        # print(f"Error code '{status_code}' not found.")
        return f"Error code '{status_code}' not found."


def build_response_headers(resource_len):
    """
    Always include Keep-alive: Close
    Alawys include Server: http_serv
    Include Content-Length header
    """

    return f"Keep-alive: Close\r\nServer: http_serv\r\nContent-Length: {resource_len}"


class HttpServer(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            print("Handling request...")

            data = self.request.recv(4096)
            print("Receive data")
            request :str= data.decode()
            print('Request:')
            print(request)

            first_line_str, req_headers_str = request.split('\r\n', maxsplit=1)

            req_headers_str = req_headers_str.replace('\r\n', '\n')

            parsed_first_line = parse_first_line(first_line_str)

            req_headers =parse_headers(req_headers_str)

            resource_path = identify_resource('http_serv/public_html', parsed_first_line['resource'])

            response_body, resource_len = read_resource(resource_path)

            status_line = build_status_line("200")
            response_headers = build_response_headers(resource_len)

            response = f'{status_line}\r\n'
            response += response_headers + '\r\n\r\n'
            response += response_body

            # response = "HTTP/1.1 204 No Content\r\n"  # CRLF \r\n \n LF

            self.request.sendall(response.encode())
        except:
            pass

def main():
    with socketserver.TCPServer(("localhost", 8095), HttpServer) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
