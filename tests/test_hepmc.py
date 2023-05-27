import pyhepmc
from feynml.interface.hepmc import hepmc_event_to_feynman

from pyfeyn2.render.all import AllRender


def test_render_hepmc():
    with pyhepmc.open("tests/example.HepMC") as f:
        for event in f:
            fd = hepmc_event_to_feynman(event)
            AllRender(fd).render()
            break


test_render_hepmc()
