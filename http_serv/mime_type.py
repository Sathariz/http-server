from enum import Enum


class MimeType(Enum):
    TEXT_HTML = 0
    TEXT_PLAIN = 1
    TEXT_CSS = 2
    APPLICATION_JSON = 3
    IMAGE_PNG = 4
    APPLICATION_OCTET_STREAM = 5

    def infer_mime_type(self, full_path):
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