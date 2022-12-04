from pyfeyn2.feynmandiagram import FeynmanDiagram, Leg, Propagator, Vertex
from pyfeyn2.render.dot import feynman_adjust_points, feynman_to_dot
from pyfeyn2.render.tikzfeynman import TikzFeynmanRender
from tests.test_feynman import test_gluons, test_many_gluons


def test_tikz():
    fd = test_gluons()

    tfd = TikzFeynmanRender(fd)
    print(tfd.get_src())
    tfd.render("test.pdf")


def test_dot_positions():
    fd = test_many_gluons()
    fd = feynman_adjust_points(fd)

    tfd = TikzFeynmanRender(fd)
    print(tfd.get_src())
    tfd.render("test.pdf")


test_tikz()
test_dot_positions()
