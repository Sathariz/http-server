

from http_serv.mime_type import MimeType


class Response:
    def __init__(self) -> None:
        self.status_code = None
        self.headers = {}
        self.content = None
        self.mime:MimeType = None
        self.content_len:int = 0

    def _fill_headers(self) -> None:
        self.headers["Server"] = "http_serv"
        self.headers["Keep-alive"] = "Close"
        self.headers["Content-type"] = self.mime.get_header_value()
        self.headers["Content-Length"] = self.content_len

    def build(self) -> bytes:
        self._fill_headers()

        CRLF = "\r\n"
        data = self.status_code.get_status_line() + CRLF
        for header_name, header_value in self.headers.items():
            data += f"{header_name}: {header_value}{CRLF}"
        data += CRLF
        data = data.encode("ascii")
        data += self.content

        return data
