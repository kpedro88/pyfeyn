from feynmodel.interface.qgraf import feynmodel_to_qgraf, qgraf_to_feynmodel
from feynmodel.interface.ufo import load_ufo_model
from pyqgraf import qgraf
from xsdata.formats.dataclass.parsers import XmlParser

from pyfeyn2.auto.bend import auto_bend
from pyfeyn2.auto.label import auto_label
from pyfeyn2.auto.position import feynman_adjust_points
from pyfeyn2.feynmandiagram import FeynmanDiagram, FeynML
from pyfeyn2.render.latex.feynmp import FeynmpRender
from pyfeyn2.render.latex.tikzfeynman import TikzFeynmanRender
from pyfeyn2.render.pyx.pyxrender import PyxRender


def auto_diagram(fd: FeynmanDiagram, scale=2, size=15):
    """
    Automatically tune a Feynman diagram from a FeynML file.
    """
    d = fd
    SCALE = scale
    d.legs[0].with_xy(-SCALE, SCALE)
    d.legs[1].with_xy(-SCALE, -SCALE)
    d.legs[2].with_xy(SCALE, SCALE)
    d.legs[3].with_xy(SCALE, -SCALE)
    d = feynman_adjust_points(d, size=15, override_vertices=False)
    auto_bend(d)
    auto_label(d.propagators)
    auto_label(d.legs)
    return d
    # print(d)
    t = TikzFeynmanRender(d)
    # print(t.get_src())
    t.render(show=True)
    # break
