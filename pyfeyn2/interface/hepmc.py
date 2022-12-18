import pyhepmc
from pyhepmc import GenEvent, GenParticle, GenVertex

from pyfeyn2.feynmandiagram import FeynmanDiagram, Leg, Propagator, Vertex


def _vertex_id_wrap(id):
    return "Vertex" + str(id).replace("-", "m")


def event_to_feynman(event):
    fd = FeynmanDiagram()
    for v in event.vertices:
        v = Vertex(id=_vertex_id_wrap(v.id))
        fd.add(v)
    for p in event.particles:
        # TODO first create all vertices?
        if p.status == 4:
            # incoming Leg
            fd.add(
                Leg(
                    id="Leg" + str(p.id).replace("-", "m"),
                    pdgid=p.pid,
                    target=_vertex_id_wrap(p.end_vertex.id),
                    sense="incoming",
                )
            )
        elif p.status == 1:
            # outgoing Leg
            fd.add(
                Leg(
                    id="Leg" + str(p.id).replace("-", "m"),
                    pdgid=p.pid,
                    target=_vertex_id_wrap(p.production_vertex.id),
                    sense="outgoing",
                )
            )
        else:
            # Propagator
            fd.add(
                Propagator(
                    id="Propagator" + str(p.id).replace("-", "m"),
                    pdgid=p.pid,
                    source=_vertex_id_wrap(p.production_vertex.id),
                    target=_vertex_id_wrap(p.end_vertex.id),
                )
            )
    return fd


def hepmc_to_feynml(hepmc_file):
    # TODO: use pyhepmc
    pass
