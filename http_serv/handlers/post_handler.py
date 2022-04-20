
from pathlib import Path
from http_serv.handlers.base_handler import BaseHandler
from http_serv.http_exceptions import Http404Exception

from http_serv.http_status import HttpStatusCode
from http_serv.mime_type import MimeType
from http_serv.request import Request
from http_serv.resources import read_resource
from http_serv.response import Response

class PostHandler(BaseHandler):
    def __init__(self, added_via_post_dir:Path) -> None:
        self.added_via_post_dir = added_via_post_dir

    def handle(self, http_request:Request) -> Response:
        self.ensure_auth(http_request)
        full_path = self.added_via_post_dir / Path(http_request.resource).name

        response = Response()

        with open(full_path, "wb") as new_file:
            new_file.write(http_request.payload)
        
        response.content = f"File {new_file.name} has been uploaded successfuly"
        response.content = response.content.encode("utf-8")
        response.content_len = len(response.content)
        response.mime = MimeType.infer_mime_type(full_path)
        response.status_code = HttpStatusCode.CREATED
        return response

