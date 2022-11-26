from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from pyfeyn2 import io_utils
from pyfeyn2.feynmandiagram import FeynmanDiagram, Propagator, Vertex


def test_print_as_xml():
    fd = FeynmanDiagram()
    fd.propagators.append(Propagator())
    fd.propagators.append(Propagator())
    fd.vertices.append(Vertex())
    fd.vertices.append(Vertex())

    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    print(serializer.render(fd))

    # io_utils.print_as_xml(fd)


test_print_as_xml()
