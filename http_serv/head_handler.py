from pathlib import Path

from http_serv.http_exceptions import Http404Exception
from http_serv.http_status import HttpStatusCode
from http_serv.resources import read_resource, get_resource_size
from http_serv.mime_type import MimeType
from http_serv.response import Response
from http_serv.request import Request


class HeadHandler:
    def __init__(self, public_html_dir: Path) -> None:
        self.public_html_dir = public_html_dir

    def handle(self, http_request: Request) -> Response:
        full_path = self.public_html_dir / http_request.resource[1:]

        if not full_path.exists():
            raise Http404Exception(http_request.resource)

        if full_path.exists() and full_path.is_dir():
            index_file = full_path / "index.html"
            if not index_file.exists():
                response = Response()
                response.mime = MimeType.TEXT_HTML.get_header_value()
                response.status_code = HttpStatusCode.OK
                return response

        if full_path.exists() and full_path.is_file():
            response = Response()
            response.content = b''
            response.content_len = get_resource_size(full_path)
            response.mime = MimeType.infer_mime_type(full_path)            
            response.status_code = HttpStatusCode.OK
            return response

