import pyhepmc

from pyhepmc import GenEvent, GenParticle, GenVertex


def event_to_feynml(event):
    for p in event.particles:
        # TODO first create all vertices?
        if p.status == 4:
            # incoming Leg

            pass
        elif p.pid== 1:
            # outgoing Leg
            pass
        else:   
            # Propagator
