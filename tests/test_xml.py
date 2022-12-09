from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from pyfeyn2.feynmandiagram import FeynmanDiagram, Leg, Propagator, Vertex


def test_print_as_xml():
    fd = FeynmanDiagram()
    v1 = Vertex("v1")
    v2 = Vertex("v2")
    p1 = Propagator("p1")
    l1 = Leg("l1")
    p1.set_source(v1)
    p1.set_target(v2)
    fd.propagators.append(p1)
    fd.vertices.append(v1)
    fd.vertices.append(v2)
    fd.legs.append(l1)

    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    print(serializer.render(fd))


test_print_as_xml()
