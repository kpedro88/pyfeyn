import pylhe
from feynml.interface.lhe import lhe_event_to_feynman

from pyfeyn2.auto.position import feynman_adjust_points
from pyfeyn2.render.all import AllRender


def test_lhe_to_feynman():
    events = pylhe.read_lhe("tests/example.lhe")
    for event in events:
        fd = lhe_event_to_feynman(event)
        fd = feynman_adjust_points(fd, clear_vertices=True)
        AllRender(fd).render()
        break
