from http_serv.http_method import HttpMethod
from http_serv.http_status import HttpStatusCode
from http_serv.mime_type import MimeType
from http_serv.response import Response


class Http404Exception(Exception):
    def __init__(self, resource):
        self.resource = resource

    def to_html(self) -> Response:
        html = Response()
        html.content = f"Could not locate {self.resource}"
        html.content = html.content.encode()
        html.content_len = len(html.content)
        html.status_code = HttpStatusCode.NOT_FOUND
        html.mime = MimeType.TEXT_HTML

        return html


class Http403Exception(Exception):
    def to_html(self) -> Response:
        html = Response()
        html.content = "You do not have permission to view this resource"
        html.content_len = len(html.content)
        html.status_code = HttpStatusCode.FORBIDDEN
        html.mime = MimeType.TEXT_HTML

        return html


class Http500Exception(Exception):
    def to_html(self) -> Response:
        html = Response()
        html.content = "Server encountered internal error"
        html.content_len = len(html.content)
        html.status_code = HttpStatusCode.INTERNAL_SERVER_ERROR
        html.mime = MimeType.TEXT_HTML

        return html


class Http405Exception(Exception):
    def __init__(self, method):
        self.method = method

    def to_html(self) -> Response:
        html = Response()
        html.content = HttpMethod.parse(self.method)
        html.content = html.content.encode()
        html.content_len = len(html.content)
        html.status_code = HttpStatusCode.METHOD_NOT_ALLOWED
        html.mime = MimeType.TEXT_HTML
        html.headers["Allow"] = "GET, POST, HEAD"

        return html


class Http401Exception(Exception):
    def to_html(self) -> Response:
        html = Response()
        html.content = "You are not authorized to view this resource"
        html.content_len = len(html.content)
        html.status_code = HttpStatusCode.UNAUTHORIZED
        html.mime = MimeType.TEXT_HTML

        return html
