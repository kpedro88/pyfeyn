import random
import string

from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic

from pyfeyn2.render.latex import LatexRender
from pyfeyn2.render.metapost import MetaPostRender
from pyfeyn2.render.render import Render

# converte FeynmanDiagram to tikz-feynman

type_map = {
    "gluon": "gluon",
    "curly": "curly",
    "dbl_curly": "dbl_curly",
    "dashes": "dashes",
    "scalar": "scalar",
    "dashes_arrow": "dashes_arrow",
    "dbl_dashes": "dbl_dashes",
    "dbl_dashes_arrow": "dbl_dashes_arrow",
    "dots": "dots",
    "dots_arrow": "dots_arrow",
    "ghost": "ghost",
    "dbl_dots": "dbl_dots",
    "dbl_dots_arrow": "dbl_dots_arrow",
    "phantom": "phantom",
    "phantom_arrow": "phantom_arrow",
    "plain": "plain",
    "plain_arrow": "plain_arrow",
    "fermion": "fermion",
    "electron": "electron",
    "quark": "quark",
    "double": "double",
    "dbl_plain": "dbl_plain",
    "double_arrow": "double_arrow",
    "dbl_plain_arrow": "dbl_plain_arrow",
    "heavy": "heavy",
    "photon": "photon",
    "boson": "boson",
    "wiggly": "wiggly",
    "dbl_wiggly": "dbl_wiggly",
    "zigzag": "zigzag",
    "dbl_zigzag": "dbl_zigzag",
}


def feynman_to_feynmp(fd):
    letters = "abcdefghijklmnopqrstuvwxyz"
    result_str = "".join(random.choice(letters) for i in range(10))
    src = "\\begin{fmffile}{tmp-" + result_str + "}\n"
    src += "\\begin{fmfgraph*}(120,80)\n"
    incoming = []
    outgoing = []
    for l in fd.legs:
        if l.sense == "incoming":
            incoming += [l]
            # src += f"\t\t\\fmfleft{{{l.id}}}\n"
            # src += f"\t\t\\fmf{{{ttype}}}{{{l.id},{l.target}}}\n"
        elif l.sense == "outgoing":
            outgoing += [l]
            # src += f"\t\t\\fmfright{{{l.id}}}\n"
            # src += f"\t\t\\fmf{{{ttype}}}{{{l.target},{l.id}}}\n"
        else:
            raise Exception("Unknown sense")
    src += "\t\t\\fmfleft{"
    for l in incoming:
        src += f"{l.id},"
    src = src[:-1]
    src += "}\n"
    src += "\t\t\\fmfright{"
    for l in outgoing:
        src += f"{l.id},"
    src = src[:-1]
    src += "}\n"

    for l in incoming:
        ttype = type_map[l.type]
        src += f"\t\t\\fmf{{{ttype}}}{{{l.id},{l.target}}}\n"
    for l in outgoing:
        ttype = type_map[l.type]
        src += f"\t\t\\fmf{{{ttype}}}{{{l.target},{l.id}}}\n"

    for p in fd.propagators:
        ttype = type_map[p.type]
        src += f"\t\t\\fmf{{{ttype}}}{{{p.source},{p.target}}}\n"
    src += "\\end{fmfgraph*}\n"
    src += "\\end{fmffile}\n"
    return src


class FeynmpRender(MetaPostRender):
    def __init__(
        self,
        fd,
        documentclass="standalone",
        document_options=["preview", "crop"],
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
        self.preamble.append(Command("usepackage", NoEscape("feynmp-auto")))
        self.set_src_diag(NoEscape(feynman_to_feynmp(fd)))

    def valid_type(typ):
        if typ.lower() in type_map:
            return True
        return False