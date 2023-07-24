import numpy as np
from feynml import FeynmanDiagram, Leg, Propagator, Vertex

from pyfeyn2.auto.position import (
    auto_align,
    auto_align_legs,
    auto_grid,
    auto_gridded_springs,
    auto_remove_intersections_by_align_legs,
    feynman_adjust_points,
)


def _get_fd_2_2():
    v1 = Vertex("v1").with_shape("dot")
    v2 = Vertex("v2").with_style("symbol : dot")

    fd = FeynmanDiagram().add(
        v1,
        v2,
        Propagator(name="g").connect(v1, v2),
        Leg(name="g").with_target(v1).with_xy(-2, 1).with_incoming(),
        Leg(name="g")
        .with_target(v2)
        .with_xy(-2, -1)
        .with_incoming()
        .with_class("notred"),
        Leg(name="g").with_target(v1).with_xy(2, 1).with_outgoing().with_class("red"),
        Leg("myid1", name="g").with_target(v2).with_xy(2, -1).with_outgoing(),
    )
    return fd


def _get_fd_2_4():
    v1 = Vertex("v1").with_shape("dot")
    v2 = Vertex("v2").with_style("symbol : dot")

    fd = FeynmanDiagram().with_rules(
        """ * {color: red;} 
            [type=fermion] {color: blue; line: gluon}
            #p1 {color: green;}
            :not([type=fermion]) { color : black; line: fermion}"""
    )
    v1 = Vertex("v1")
    v2 = Vertex("v2")
    v3 = Vertex("v3")
    v4 = Vertex("v4")
    p1 = Propagator("p1").connect(v1, v2).with_type("gluon")
    p2 = Propagator("p2").connect(v1, v3).with_type("gluon")
    p3 = Propagator("p3").connect(v3, v2).with_type("gluon")
    p4 = Propagator("p4").connect(v4, v3).with_type("gluon")
    p5 = Propagator("p5").connect(v4, v2).with_type("gluon")
    l1 = Leg("l1").with_target(v1).with_type("gluon").with_incoming().with_xy(2, 1)
    l2 = Leg("l2").with_target(v1).with_type("gluon").with_incoming().with_xy(-2, -1)
    l3 = (
        Leg("l3")
        .with_target(v2)
        .with_type("fermion")
        .with_outgoing()
        .with_xy(2, -2)
        .with_class("blue")
    )
    l4 = Leg("l4").with_target(v3).with_type("fermion").with_outgoing().with_xy(2, 2)
    l5 = Leg("l5").with_target(v4).with_type("gluon").with_outgoing().with_xy(2, 1)
    l6 = Leg("l6").with_target(v4).with_type("gluon").with_outgoing().with_xy(-2, -1)

    l6.style.color = "orange"

    fd.propagators.extend([p1, p2, p3, p4, p5])
    fd.vertices.extend([v1, v2, v3, v4])
    fd.legs.extend([l1, l2, l3, l4, l5, l6])
    return fd


def test_auto_grid():
    fd = _get_fd_2_2()
    fd = feynman_adjust_points(fd, size=10)
    fd = auto_grid(fd, n_x=3, n_y=4)


def test_auto_align():
    fd = _get_fd_2_2()
    fd = feynman_adjust_points(fd, size=10)
    fd = auto_align(
        fd, np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [0, -0.05], [0.0, 0.05]]) * 2
    )


def test_auto_align_legs():
    fd = _get_fd_2_4()
    fd = feynman_adjust_points(fd, size=10)
    fd = auto_align_legs(fd)


def test_auto_remove_intersections_by_align_legs():
    fd = _get_fd_2_4()
    fd = feynman_adjust_points(fd, size=10)
    fd = auto_remove_intersections_by_align_legs(fd)


def test_auto_gridded_springs():
    fd = _get_fd_2_4()
    fd = feynman_adjust_points(fd, size=10)
    fd = auto_gridded_springs(fd)
