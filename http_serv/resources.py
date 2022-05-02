from pathlib import Path


def read_resource(resource_path: Path) -> bytes:
    with resource_path.open("rb") as f:
        data = f.read()

    return data

def get_resource_size(resource_path: Path)->int:
    return Path(resource_path).stat().st_size
