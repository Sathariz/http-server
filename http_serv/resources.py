from pathlib import Path


def read_resource(resource_path: Path) -> bytes:
    with resource_path.open("rb") as f:
        data = f.read()

    return data
