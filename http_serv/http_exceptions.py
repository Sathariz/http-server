class Http404Exception(Exception):
    def __init__(self, resource):
        self.resource = resource


class Http500Exception(Exception):
    pass
