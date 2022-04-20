from crypt import methods
import socketserver, os
from pathlib import Path

from http_serv.http_exceptions import (
    Http403Exception,
    Http404Exception,
    Http405Exception,
)
from http_serv.http_status import HttpStatusCode
from http_serv.request import Request
from http_serv.response import Response
from http_serv.http_method import HttpMethod
from http_serv.handlers import HeadHandler, GetHandler, PostHandler



class HttpServer(socketserver.BaseRequestHandler):
    def handle(self):

        raw_request = self.request.recv(4096)
        print("Request data:")
        print(raw_request)

        http_request = Request(raw_request)

        match http_request.method:
            case HttpMethod.GET:
                handler = GetHandler(Path("public_html"))
            case HttpMethod.HEAD:
                handler = HeadHandler(Path("public_html"))
            case HttpMethod.POST:
                handler = PostHandler(Path("public_html/added_via_POST"))
            case _:
                raise Http405Exception(http_request.method)

        print(http_request)

        # handler = PostHandler(Path("public_html/added_via_POST"))
        # handler = HeadHandler(Path("public_html"))
        
        http_response = handler.handle(http_request)
        raw_response = http_response.build()

        self.request.sendall(raw_response)


def main():
    with socketserver.TCPServer(("localhost", 8092), HttpServer) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
