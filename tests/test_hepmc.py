import pyhepmc
from feynml.interface.hepmc import hepmc_event_to_feynman

from pyfeyn2.auto.position import feynman_adjust_points
from pyfeyn2.render.latex.tikzfeynman import TikzFeynmanRender


def test_render_hepmc():
    with pyhepmc.open("tests/example.HepMC") as f:
        for event in f:
            fd = hepmc_event_to_feynman(event)
            fd = feynman_adjust_points(fd, clear_vertices=True)
            TikzFeynmanRender(fd).render()
            break


# test_render_hepmc()
