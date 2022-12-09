from pathlib import Path

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

# Load an FML file and check that it is the same as the original
# FeynmanDiagram object
from pyfeyn2.feynmandiagram import (
    FeynmanDiagram,
    FeynML,
    Head,
    Leg,
    Meta,
    Propagator,
    Vertex,
)
from pyfeyn2.render.pyx.pyxrender import PyxRender


def test_print_fml():
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

    fml = FeynML(
        head=Head(
            metas=Meta(name="pyfeyn2", value="test"),
            description="Simple single test diagram",
        ),
        diagrams=[fd],
    )
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    print(serializer.render(fml))


def test_load_fml():
    xml_string = Path("tests/test.fml").read_text()
    parser = XmlParser()
    fd = parser.from_string(xml_string, FeynML)
    print(fd)


def test_plot_fml():
    xml_string = Path("tests/test.fml").read_text()
    parser = XmlParser()
    fml = parser.from_string(xml_string, FeynML)
    PyxRender(fml.diagrams[0]).render()


test_print_fml()
test_load_fml()
test_plot_fml()
