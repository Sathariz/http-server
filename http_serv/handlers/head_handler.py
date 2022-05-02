from pathlib import Path
from http_serv.handlers.base_handler import BaseHandler

from http_serv.http_exceptions import Http404Exception
from http_serv.http_status import HttpStatusCode
from http_serv.resources import get_resource_size
from http_serv.mime_type import MimeType
from http_serv.response import Response
from http_serv.request import Request


class HeadHandler(BaseHandler):
    def __init__(self, public_html_dir: Path) -> None:
        self.public_html_dir = public_html_dir

    def handle(self, http_request: Request) -> Response:
        self.ensure_auth(http_request)
        exists, location = self.identify_resource_strategy(http_request.resource)

        if exists:
            content_len = get_resource_size(location)
        else:
            content_len = len(self.index_list_generator(location))

        response = Response()
        response.content = b''
        response.content_len = content_len
        response.mime = MimeType.infer_mime_type(location) if exists else MimeType.TEXT_HTML
        response.status_code = HttpStatusCode.OK

        return response

