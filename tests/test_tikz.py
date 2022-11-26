from pyfeyn2.feynmandiagram import FeynmanDiagram, Leg, Propagator, Vertex
from pyfeyn2.render.tikzfeynman import TikzFeynmanRender


def test_tikz():
    fd = FeynmanDiagram()
    v1 = Vertex("v1").set_xy(-1, 0)
    v2 = Vertex("v2").set_xy(1, 0)
    p1 = Propagator("p1").connect(v1, v2).set_type("gluon")
    l1 = Leg("l1").set_target(v1).set_xy(-2, 1).set_type("gluon")
    l2 = Leg("l2").set_target(v1).set_xy(-2, -1).set_type("gluon")
    l3 = Leg("l3").set_target(v2).set_xy(2, 1).set_type("gluon")
    l4 = Leg("l4").set_target(v2).set_xy(2, -1).set_type("gluon")

    p1.set_source(v1)
    p1.set_target(v2)
    fd.propagators.append(p1)
    fd.vertices.extend([v1, v2])
    fd.legs.extend([l1, l2, l3, l4])
    tfd = TikzFeynmanRender(fd)
    print(tfd.get_src())
    tfd.render("test.pdf")


test_tikz()
