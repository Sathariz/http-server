from pathlib import Path

from http_serv.http_exceptions import Http404Exception
from http_serv.http_status import HttpStatusCode
from http_serv.mime_type import MimeType
from http_serv.request import Request
from http_serv.resources import read_resource
from http_serv.response import Response


class GetHandler:
    def __init__(self, public_html_dir:Path) -> None:
        self.public_html_dir = public_html_dir

    def handle(self, http_request:Request) -> Response:

        full_path = self.public_html_dir / http_request.resource[1:]

        if not full_path.exists():
            raise Http404Exception(http_request.resource)

        if full_path.exists() and full_path.is_dir():
            index_file = full_path / "index.html"
            if not index_file.exists():
                listing = self._index_list_generator(full_path)
                response = Response()
                response.content = listing.encode("utf-8")
                response.content_len = len(response.content)
                response.mime = MimeType.TEXT_HTML.get_header_value()
                response.status_code = HttpStatusCode.OK
                return response

        if full_path.exists() and full_path.is_file():
            response = Response()
            response.content = read_resource(full_path)
            response.content_len = len(response.content)
            response.mime = MimeType.infer_mime_type(full_path)
            response.status_code = HttpStatusCode.OK
            return response

        # ...

    def _index_list_generator(self, current_dir_path: Path) -> str:
        # HARDCODED!!!
        # dir_path = os.path.join("public_html", current_dir_path.strip("/"))

        # give it nice formatting  style='margin-left:90px;
        html_code = (
            "<center><table><tr><th>File Name</th><th>Link</th><th>Path</th></tr>"
        )

        for f in current_dir_path.iterdir():
            file_name = f.name
            url = "/" + "/".join((f.parts[1:]))
            html_code += f"<tr><td>{file_name}</td><td><a href='{url}' target=_blank>{file_name.split('.')[0]}</a></td><td>{f}</td></tr>"
        html_code += "</table></center>"

        # html_code = html_code.encode()  # ??

        return html_code

