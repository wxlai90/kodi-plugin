class Params:
    def __init__(self) -> None:
        self.params = {}

    def path(self, p):
        if callable(p):
            p = p.__name__
        self.params['path'] = p
        return self

    def set(self, k, v):
        self.params[k] = v
        return self

    def asDict(self):
        return self.params
