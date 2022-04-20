from pathlib import Path
from typing import Tuple
from http_serv.http_exceptions import Http404Exception
from http_serv.request import Request
from http_serv.response import Response

from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @abstractmethod
    def handle(self, http_request: Request) -> Response:
        pass

    def identify_resource_strategy(self, resource:str) -> Tuple[bool, Path]:
        '''
        1. 404 -> rzuć wyjątek
        2. resource jest plikiem -> zwróć ścieżkę do tego pliku
        3. resource jest katalogiem i ma index.html -> zwróć ścieżkę do tego pliku
        4. resource jest katalogiem i nie ma index.html -> None
        '''
        full_path = self.public_html_dir / resource[1:]

        if full_path.exists() and full_path.is_file():
            return True, full_path
        
        if full_path.exists() and full_path.is_dir():
            index = full_path / 'index.html'
            if index.exists():
                return True, index
            else:
                return False, full_path
        
        if not full_path.exists():
            raise Http404Exception(resource)

        assert False

    def index_list_generator(self, current_dir_path: Path) -> bytes:
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

        html_code = html_code.encode()  # ??

        return html_code
    