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
from http_serv.get_handler import GetHandler
from http_serv.post_handler import PostHandler
from http_serv.head_handler import HeadHandler


class HttpServer(socketserver.BaseRequestHandler):
    def handle(self):

        raw_request = self.request.recv(4096)
        print("Request data:")
        print(raw_request)

        http_request = Request(raw_request)
        print(http_request)

        handler = GetHandler(Path("public_html"))
        # handler = PostHandler(Path("public_html/added_via_POST"))
        # handler = HeadHandler(Path("public_html"))
        
        http_response = handler.handle(http_request)
        raw_response = http_response.build()

        self.request.sendall(raw_response)


def main():
    with socketserver.TCPServer(("localhost", 8095), HttpServer) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
