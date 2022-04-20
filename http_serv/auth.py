import base64
from pathlib import Path
from typing import Union, Any, Optional

def is_auth_required(resource:Path) -> bool:
    auth_required = "secret" in str(resource)
    return auth_required


def authorized(headers: dict[str, str]) -> bool:
    if "Authorization" not in headers:
        return False

    encoded = headers["Authorization"].split()[1]
    decoded = base64.b64decode(encoded)

    valid = decoded == b"john:doe"
    return valid
