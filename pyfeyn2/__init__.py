from importlib.metadata import version

from pyfeyn2.render.latex.dot import DotRender
from pyfeyn2.render.latex.feynmp import FeynmpRender
from pyfeyn2.render.latex.tikzfeynman import TikzFeynmanRender
from pyfeyn2.render.mpl.feynmanrender import FeynmanRender
from pyfeyn2.render.mpl.mpl import MPLRender
from pyfeyn2.render.pyx.pyxrender import PyxRender
from pyfeyn2.render.text.asciipdf import ASCIIPDFRender
from pyfeyn2.render.text.unicodepdf import UnicodePDFRender

package = "pyfeyn2"

__version__ = version(package)


renders = {
    "pyx": PyxRender,
    "feynmp": FeynmpRender,
    "tikz": TikzFeynmanRender,
    "dot": DotRender,
    "feynman": FeynmanRender,
    "mpl": MPLRender,
    "ascii": ASCIIPDFRender,
    "unicode": UnicodePDFRender,
}
styles = [
    "color",
    "opacity",
    "arrow-pos",
    "parallel-arrow-sense",
    "parallel-arrow-displace",
]
types = [
    # General
    "fermion",
    "boson",
    "vector",
    "scalar",
    # SM
    "photon",
    "higgs",
    "gluon",
    "ghost",
    # Grav
    "graviton",
    # MSSM
    "gluino",
    "squark",
    "slepton",
    "gaugino",
    "neutralino",
    "chargino",
    "higgsino",
    "gravitino",
    # util
    "phantom",
]
attributes = [
    "x",
    "y",
    # "bend",
    "label",
    "pdgid",
    "style",
    "type",
    "text",
    "momentum",
    "tension",
]
