from enum import Enum
from pathlib import Path


class MimeType(Enum):
    TEXT_HTML = 0
    TEXT_PLAIN = 1
    TEXT_CSS = 2
    APPLICATION_JSON = 3
    IMAGE_PNG = 4
    APPLICATION_OCTET_STREAM = 5

    def get_header_value(self):
        match self:
            case MimeType.TEXT_HTML:
                return 'text/html'
            case MimeType.TEXT_PLAIN:
                return 'text/plain'
            case MimeType.TEXT_CSS:
                return 'text/css'
            case MimeType.APPLICATION_JSON:
                return 'application/json'
            case MimeType.IMAGE_PNG:
                return 'image/png'
            case MimeType.APPLICATION_OCTET_STREAM:
                return 'application/octet-stream'
            case _:
                raise ValueError(f"Unknow MIME Type {self}")

    @classmethod
    def infer_mime_type(cls, full_path:Path):
        match full_path.suffix:
            case ".html":
                return MimeType.TEXT_HTML
            case ".txt":
                return MimeType.TEXT_PLAIN
            case ".css":
                return MimeType.TEXT_CSS
            case ".json":
                return MimeType.APPLICATION_JSON
            case ".png":
                return MimeType.IMAGE_PNG
            case _:
                return MimeType.APPLICATION_OCTET_STREAM