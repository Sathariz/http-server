import base64


def is_auth_required(resource):
    auth_required = "secret" in resource
    return auth_required


def authorized(headers):
    if "Authorization" not in headers:
        return False

    encoded = headers["Authorization"].split()[1]
    decoded = base64.b64decode(encoded)

    return decoded == b"john:doe"
