from enum import Enum

# from http_serv.http_exceptions import Http405Exception


class HttpMethod(Enum):
    HEAD = 0
    GET = 1
    POST = 2

    @classmethod
    def parse(cls, string):
        match string:
            case "HEAD":
                return HttpMethod.HEAD
            case "GET":
                return HttpMethod.GET
            case "POST":
                return HttpMethod.POST
            case _:
                # raise Http405Exception(f"Unsupported http method {string}")
                raise Exception(b"Method error")
