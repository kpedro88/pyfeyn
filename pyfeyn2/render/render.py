class Render:
    def __init__(self, fd):
        self.fd = fd
        self.src = ""

    def get_src(self):
        return self.src

    def render(self, file=None):
        pass

    def valid_style(style):
        return False

    def valid_type(style):
        return False

    def valid_attribute(style):
        return False
