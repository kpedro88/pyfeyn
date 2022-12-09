from pyfeyn2.render.dot import DotRender, feynman_to_dot
from tests.test_feynman import test_gluons, test_many_gluons


def test_dot():
    fd = test_gluons()

    print(feynman_to_dot(fd))
    dr = DotRender(fd)
    print(dr.get_src())
    dr.render("test.pdf")


def test_dot2():
    fd = test_many_gluons()

    print(feynman_to_dot(fd))
    dr = DotRender(fd)
    print(dr.get_src())
    dr.render("test.pdf")


test_dot()
test_dot2()
