class Render:
    def __init__(self, fd):
        self.fd = fd
        self.src = ""

    def get_src(self):
        return self.src

    def render(self, file=None):
        pass

    def valid_style(style: str) -> bool:
        return False

    def valid_type(typ: str) -> bool:
        return False

    def valid_attribute(attr: str) -> bool:
        return False
