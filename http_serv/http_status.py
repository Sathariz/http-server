from enum import Enum

# from http_serv.http_exceptions import Http500Exception


class HttpStatusCode(Enum):
    OK = (200,)
    CREATED = (201,)
    NO_CONTENT = (204,)
    UNAUTHORIZED = (401,)
    FORBIDDEN = (403,)
    NOT_FOUND = (404,)
    METHOD_NOT_ALLOWED = (405,)
    INTERNAL_SERVER_ERROR = (500,)

    def get_status_line(self):
        match self:
            case HttpStatusCode.OK:
                return "HTTP/1.1 200 OK"
            case HttpStatusCode.NOT_FOUND:
                return "HTTP/1.1 404 Not Found"
            case HttpStatusCode.METHOD_NOT_ALLOWED:
                return "HTTP/1.1 405 Method Not Allowed"
            case HttpStatusCode.FORBIDDEN:
                return "HTTP/1.1 403 Forbidden"
            case HttpStatusCode.UNAUTHORIZED:
                return "HTTP/1.1 401 Unauthorized"
            case HttpStatusCode.INTERNAL_SERVER_ERROR:
                return "HTTP/1.1 500 Internal Server Error"
            case HttpStatusCode.CREATED:
                return "HTTP/1.1 201 Created"
            case HttpStatusCode.NO_CONTENT:
                return "HTTP/1.1 204 No Content"
            case _:
                # raise Http500Exception("Status code cannot be formatted as status line")
                raise Exception(b"Status Code Error")
