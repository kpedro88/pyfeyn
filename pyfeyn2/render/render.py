from pyfeyn2.feynmandiagram import FeynmanDiagram, Leg, Propagator, Vertex


class Render:
    def __init__(self, fd=None):
        self.fd = fd
        self.src = ""

    def set_feynman_diagram(self, fd):
        self.fd = fd

    def get_src(self):
        return self.src

    def set_src(self, src):
        self.src = src

    def render(self, file=None, show=True, resolution=100, width=None, height=None):
        pass

    def valid_style(self, style: str) -> bool:
        return False

    def valid_type(self, typ: str) -> bool:
        return False

    def valid_attribute(self, attr: str) -> bool:
        if attr in ["id", "pdgid", "sense", "target", "source", "type"]:
            return True
        return False

    def demo_propagator(self, d, show=True, label=None):
        v1 = Vertex().set_xy(-2, -2)
        v2 = Vertex().set_xy(2, -2)

        fd = FeynmanDiagram().add(
            v1,
            v2,
            Propagator().connect(v1, v2).set_type(d).set_label(label).set_tension(0.0),
            Leg()
            .set_target(v1)
            .set_point(v1)
            .set_type("phantom")
            .set_incoming()
            .set_length(0.0),
            Leg()
            .set_target(v2)
            .set_point(v2)
            .set_type("phantom")
            .set_outgoing()
            .set_length(0.0),
        )

        self.set_feynman_diagram(fd)
        self.render(show=show)
