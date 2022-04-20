from pathlib import Path


def read_resource(resource_path: Path) -> bytes:
    with resource_path.open("rb") as f:
        data = f.read()

    return data

def get_resource_size(resource_path: Path)->int:
    return 17 # TODO: how to read file size in bytes?
