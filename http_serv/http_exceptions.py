class Http404Exception(Exception):
    def __init__(self, resource):
        self.resource = resource

class Http403Exception(Exception):
    pass

class Http500Exception(Exception):
    pass
