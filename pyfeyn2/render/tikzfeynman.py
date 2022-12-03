from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic

from pyfeyn2.render.latex import LatexRender
from pyfeyn2.render.render import Render

# converte FeynmanDiagram to tikz-feynman

type_map = {
    "gluon": "gluon",
    "ghost": "ghost",
    "photon": "boson",
    "boson": "boson",
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
}


def feynman_to_tikz_feynman(fd):
    src = "\\begin{tikzpicture}\n"
    src += "\\begin{feynman}\n"
    for v in fd.vertices:
        src += f"\t\\vertex ({v.id}) [label={v.label}] at ({v.x},{v.y});\n"
    for l in fd.legs:
        src += f"\t\\vertex ({l.id}) [label={l.label}] at ({l.x},{l.y});\n"
    src += "\t\\diagram*{\n"
    for p in fd.propagators:
        ttype = type_map[p.type]
        src += f"\t\t({p.source}) -- [{ttype}] ({p.target}),\n"
    for l in fd.legs:
        ttype = type_map[l.type]
        if l.sense == "incoming":
            src += f"\t\t({l.id}) -- [{ttype}] ({l.target}),\n"
        elif l.sense == "outgoing":
            src += f"\t\t({l.target}) -- [{ttype}] ({l.id}),\n"
        else:
            raise Exception("Unknown sense")
    src += "\t};\n"
    src += "\\end{feynman}\n"
    src += "\\end{tikzpicture}\n"
    return src


class TikzFeynmanRender(LatexRender):
    def __init__(
        self,
        fd,
        documentclass="standalone",
        document_options=["preview", "crop", "tikz"],
        *args,
        **kwargs,
    ):
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
        self.set_src_diag(NoEscape(feynman_to_tikz_feynman(fd)))

    def valid_type(typ):
        if typ.lower() in type_map:
            return True
        return False
