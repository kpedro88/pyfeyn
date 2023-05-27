import pylhe
from feynml.interface.lhe import lhe_event_to_feynman

from pyfeyn2.render.all import AllRender


def test_lhe_to_feynman():
    events = pylhe.read_lhe("tests/example.lhe")
    for event in events:
        fd = lhe_event_to_feynman(event)
        AllRender(fd).render()
        break
