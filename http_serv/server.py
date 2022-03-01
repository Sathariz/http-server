import socketserver, os
from pathlib import Path

from http_serv.http_exceptions import Http404Exception
from http_serv.http_status import HttpStatusCode
from http_serv.utils import (
    parse_first_line,
    parse_headers,
    build_response_headers,
    build_status_line,
    identify_resource,
    read_resource,
)


class HttpServer(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            print("Handling request...")

            data = self.request.recv(4096)
            print("Receive data")
            request: str = data.decode()
            print("Request:")
            print(request)

            try:
                first_line_str, req_headers_str = request.split("\r\n", maxsplit=1)
                req_headers_str = req_headers_str.replace("\r\n", "\n")
                parsed_first_line = parse_first_line(first_line_str)
                req_headers = parse_headers(req_headers_str)

                ####

                resource_path = identify_resource(
                    "http_serv/public_html", parsed_first_line["resource"]
                )
                response_body, resource_len = read_resource(resource_path)

                ###

                status_line = build_status_line(HttpStatusCode.OK)
                response_headers = build_response_headers(resource_len)

            except Http404Exception as e:
                status_line = build_status_line(HttpStatusCode.NOT_FOUND)
                response_body = (
                    f"<h1>404 Not Found</h1>\nCannot found resource {e.resource}"
                )
                response_headers = build_response_headers(len(response_body))  # ?
            except Exception as e:
                status_line = build_status_line(HttpStatusCode.INTERNAL_SERVER_ERROR)
                response_headers = build_response_headers(0)  # ?
                response_body = ""

            ###

            response = f"{status_line}\r\n"
            response += response_headers + "\r\n\r\n"
            response += response_body

            ###

            self.request.sendall(response.encode())
        except:
            pass


def main():
    with socketserver.TCPServer(("localhost", 8091), HttpServer) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
