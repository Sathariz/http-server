from http_serv.http_method import HttpMethod


class Request:
    def __init__(self, raw_request:bytes) -> None:
        self.method :HttpMethod = None
        self.resource = None
        self.headers = {}
        self.content = None

        preamble, self.payload = raw_request.split(b"\r\n\r\n", maxsplit=1)
        preamble = preamble.decode().replace("\r\n", "\n")

        first_line, headers_string = preamble.split("\n", maxsplit=1)

        self._parse_first_line(first_line)
        self._parse_headers(headers_string)

    def _parse_first_line(self, first_line:str) -> None:
        method_string = first_line.split()[0]
        self.method = HttpMethod.parse(method_string)

        self.resource = first_line.split()[1]
        _ = first_line.split()[2]

    def _parse_headers(self, request_str:str) -> None:
        lines = request_str.split("\n")
        self.headers = {}
        for line in lines:
            if line.strip() == "":
                continue

            temp = line.split(": ", 1)
            self.headers[temp[0]] = temp[1]

    def __str__(self) -> str:
        return f"{self.method} request on resource {self.resource}"
