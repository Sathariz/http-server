from enum import Enum

# class HttpStatusCode(Enum):
#     HTTP_200 = 200,
#     HTTP_201 = 201,
#     HTTP_404 = 404,
#     HTTP_500 = 500,


class HttpStatusCode(Enum):
    OK = (200,)
    CREATED = (201,)
    NO_CONTENT = (204,)
    UNAUTHORIZED = (401,)
    FORBIDDEN = (403,)
    NOT_FOUND = (404,)
    METHOD_NOT_ALLOWED = (405,)
    INTERNAL_SERVER_ERROR = (500,)
