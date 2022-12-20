from typing import List

from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.feynmandiagram import Connector, FeynmanDiagram, Leg, Vertex
from pyfeyn2.render.latex.latex import LatexRender

# converte FeynmanDiagram to tikz-feynman

type_map = {
    "gluon": "gluon",
    "ghost": "ghost",
    "photon": "photon",
    "boson": "photon",
    "fermion": "fermion",
    "anti fermion": "anti fermion",
    "charged boson": "charged boson",
    "anti charged boson": "anti charged boson",
    "scalar": "scalar",
    "charged scalar": "charged scalar",
    "anti charged scalar": "anti charged scalar",
    "majorana": "majorana",
    "anti majorana": "anti majorana",
    # SUSY
    "gaugino": "plain,boson",
    "chargino": "plain,boson",
    "neutralino": "plain,boson",
    "squark": "charged scalar",
    "slepton": "charged scalar",
    "gluino": "plain,gluon",
    "higgs": "scalar",
    "vector": "boson",
    # UTIL
    "phantom": "draw=none",
    "line": "plain",
    "plain": "plain",
}


def stylize_connect(fd: FeynmanDiagram, c: Connector):
    style = fd.get_style(c)
    ret = ""
    ret += type_map[style.getProperty("line").value]

    if c.label is not None:
        ret += ",edge label=" + c.label
    # if c.edge_label_ is not None: style += ",edge label'=" + c.edge_label_
    if (
        style.getProperty("momentum-arrow") is not None
        and style.getProperty("momentum-arrow").value == "true"
    ):
        ret += ",momentum=" + c.momentum
    if style.opacity is not None and style.opacity != "":
        ret += ",opacity=" + str(style.opacity)
    if style.color is not None and style.color != "":
        ret += "," + str(style.color)
    if style.getProperty("bend-direction") is not None:
        ret += ",bend " + str(style.getProperty("bend-direction").value)
    if style.getProperty("bend-loop") is not None:
        ret += (
            ",loop , in="
            + str(style.getProperty("bend-in").value)
            + ", out="
            + str(style.getProperty("bend-out").value)
            + ", min distance="
            + str(style.getProperty("bend-min-distance").value)
        )

    return ret


def stylize_node(v: Vertex):
    style = ""
    if v.label is not None:
        style += "label=" + v.label + ","

    return style[:-1]


def stylize_leg_node(l: Leg):
    style = ""
    if l.external is not None:
        style += "label=" + l.external + ","
    return style[:-1]


def get_line(source_id, target_id, style):
    # Fix self-loop
    if source_id == target_id:
        return f"\t\t({source_id}) -- [{style}] ({target_id}clone),\n"
    else:
        return f"\t\t({source_id}) -- [{style}] ({target_id}),\n"


def feynman_to_tikz_feynman(fd):
    src = "\\begin{tikzpicture}\n"
    src += "\\begin{feynman}\n"
    for v in fd.vertices:
        style = stylize_node(v)
        src += f"\t\\vertex ({v.id}) [{style}] at ({v.x},{v.y});\n"
        src += f"\t\\vertex ({v.id}clone) [{style}] at ({v.x},{v.y});\n"
    for l in fd.legs:
        style = stylize_leg_node(l)
        src += f"\t\\vertex ({l.id}) [{style}] at ({l.x},{l.y});\n"
    src += "\t\\diagram*{\n"
    for p in fd.propagators:
        style = stylize_connect(fd, p)
        src += get_line(p.source, p.target, style)
    for l in fd.legs:
        style = stylize_connect(fd, l)
        if l.sense[:2] == "in":
            src += get_line(l.id, l.target, style)
        elif l.sense[:3] == "out":
            src += get_line(l.target, l.id, style)
        else:
            raise Exception("Unknown sense")
    src += "\t};\n"
    src += "\\end{feynman}\n"
    src += "\\end{tikzpicture}\n"
    return src


class TikzFeynmanRender(LatexRender):
    def __init__(
        self,
        fd=None,
        documentclass="standalone",
        document_options=None,
        *args,
        **kwargs,
    ):
        if document_options is None:
            document_options = ["preview", "crop", "tikz"]
        super().__init__(
            *args,
            fd=fd,
            documentclass=documentclass,
            document_options=document_options,
            **kwargs,
        )
        self.preamble.append(Command("RequirePackage", "luatex85"))
        self.preamble.append(
            Command("usepackage", NoEscape("tikz-feynman"), "compat=1.1.0")
        )
        if fd is not None:
            self.set_feynman_diagram(fd)

    def set_feynman_diagram(self, fd):
        super().set_feynman_diagram(fd)
        self.set_src_diag(NoEscape(feynman_to_tikz_feynman(fd)))

    @classmethod
    def valid_styles(cls) -> bool:
        return super(TikzFeynmanRender, cls).valid_styles() + [
            "color",
            "opacity",
            "bend",
            "bend-direction",
            "bend-in",
            "bend-out",
            "bend-loop",
            "bend-min-distance",
            "momentum-arrow",
        ]

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return super(TikzFeynmanRender, cls).valid_attributes() + [
            "x",
            "y",
            "label",
            "style",
        ]

    @classmethod
    def valid_types(cls) -> List[str]:
        return super(TikzFeynmanRender, cls).valid_types() + list(type_map.keys())
