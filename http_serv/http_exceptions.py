class Http404Exception(Exception):
    def __init__(self, resource):
        self.resource = resource


class Http403Exception(Exception):
    pass


class Http500Exception(Exception):
    pass


class Http405Exception(Exception):
    def __init__(self, method):
        self.method = method
