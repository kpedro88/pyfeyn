from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.feynmandiagram import Connector, Vertex
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
    "phantom": "draw=none",
}


def stylize_connect(c: Connector):
    style = ""
    style += type_map[c.type]

    if c.label is not None:
        style += ",edge label=" + c.label
    # if c.edge_label_ is not None: style += ",edge label'=" + c.edge_label_
    if c.momentum is not None:
        style += ",momentum=" + c.momentum
    if c.style.opacity is not None and c.style.opacity != "":
        style += ",opacity=" + str(c.style.opacity)
    if c.style.color is not None and c.style.color != "":
        style += "," + str(c.style.color)

    return style


def stylize_node(v: Vertex):
    style = ""
    if v.label is not None:
        style += "label=" + v.label
    return style


def feynman_to_tikz_feynman(fd):
    src = "\\begin{tikzpicture}\n"
    src += "\\begin{feynman}\n"
    for v in fd.vertices:
        style = stylize_node(v)
        src += f"\t\\vertex ({v.id}) [{style}] at ({v.x},{v.y});\n"
    for l in fd.legs:
        # style = stylize_node(l)
        src += f"\t\\vertex ({l.id}) [{style}] at ({l.x},{l.y});\n"
    src += "\t\\diagram*{\n"
    for p in fd.propagators:
        style = stylize_connect(p)
        src += f"\t\t({p.source}) -- [{style}] ({p.target}),\n"
    for l in fd.legs:
        style = stylize_connect(l)
        if l.sense[:2] == "in":
            src += f"\t\t({l.id}) -- [{style}] ({l.target}),\n"
        elif l.sense[:3] == "out":
            src += f"\t\t({l.target}) -- [{style}] ({l.id}),\n"
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

    @staticmethod
    def valid_styles(style: str) -> bool:
        return super(TikzFeynmanRender, TikzFeynmanRender).valid_styles(
            style
        ) or style in ["color", "opacity"]

    @staticmethod
    def valid_attribute(attr: str) -> bool:
        return super(TikzFeynmanRender, TikzFeynmanRender).valid_attribute(
            attr
        ) or attr in ["x", "y", "label","style"]

    @staticmethod
    def valid_type(typ):
        if typ.lower() in type_map:
            return True
        return False
