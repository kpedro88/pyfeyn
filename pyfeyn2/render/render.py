class Render:
    def __init__(self, fd):
        self.fd = fd
        self.src = ""

    def get_src(self):
        return self.src

    def render(self, file=None):
        pass

    def valid_style(self, style: str) -> bool:
        return False

    def valid_type(self, typ: str) -> bool:
        return False

    def valid_attribute(self, attr: str) -> bool:
        if attr == "id":
            return True
        if attr == "sense":
            return True
        if attr == "target":
            return True
        if attr == "source":
            return True
        if attr == "type":
            return True
        return False
