import copy

import dot2tex
from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.feynmandiagram import Connector
from pyfeyn2.render.latex.latex import LatexRender

# workaround for dot2tex bug in math mode labels
REPLACE_THIS_WITH_A_BACKSLASH = "¬"
# https://tikz.dev/tikz-decorations
map_feyn_to_tikz = {
    "vector": "decorate,decoration=snake",
    "boson": "decorate,decoration=snake",
    "photon": "decorate,decoration=snake",
    "gluon": "decorate,decoration={coil,aspect=0.3,segment length=1mm}",
    "ghost": "dotted",
    "fermion": "decorate,postaction={decorate,draw,red,decoration={markings,mark=at position 0.5 with {\\arrow{>}}}}",
    "higgs": "densely dashed",
    "scalar": "densely dashed",
    "slepton": "densely dashed",
    "squark": "densely dashed",
    "zigzag": "decorate,decoration=zigzag",
    "phantom": "draw=none",
}


def stylize_connect(c: Connector) -> str:
    style = 'style="{}",texmode="raw"'.format(map_feyn_to_tikz[c.type])
    if c.label is None:
        label = ""
    else:
        label = c.label.replace("\\", REPLACE_THIS_WITH_A_BACKSLASH)
    if c.length is not None:
        style += f",len={c.length}"
    style += f',label="{label}"'
    return style


def feynman_adjust_points(feyndiag, size=5, delete_vertices=True):
    # deepcopy
    fd = copy.deepcopy(feyndiag)
    if delete_vertices:
        for v in fd.vertices:
            v.x = None
            v.y = None
    norm = size
    dot = feynman_to_dot(fd)
    positions = dot_to_positions(dot)
    mmax = 0
    for _, p in positions.items():
        if p[0] > mmax:
            mmax = p[0]
        if p[1] > mmax:
            mmax = p[1]
    for v in fd.vertices:
        if v.id in positions:
            v.x = positions[v.id][0] / mmax * norm
            v.y = positions[v.id][1] / mmax * norm
    for l in fd.legs:
        l.x = positions[l.id][0] / mmax * norm
        l.y = positions[l.id][1] / mmax * norm
    return fd


def dot_to_positions(dot):
    return dot2tex.dot2tex(dot, format="positions")


def dot_to_tikz(dot):
    ret = dot2tex.dot2tex(dot, format="tikz", figonly=True)
    ret = ret.replace(REPLACE_THIS_WITH_A_BACKSLASH, "\\")
    return ret


def feynman_to_dot(fd):
    # TODO better use pydot? still alive?
    # TODO style pick neato or dot or whatever
    src = "graph G {\n"
    src += "rankdir=LR;\n"
    src += "layout=neato;\n"
    # src += "mode=hier;\n"
    src += 'node [style="invis"];\n'
    for l in fd.legs:
        if l.x is not None and l.y is not None:
            src += f'\t\t{l.id} [ pos="{l.x},{l.y}!"];\n'
    for l in fd.vertices:
        if l.x is not None and l.y is not None:
            src += f'\t\t{l.id} [ pos="{l.x},{l.y}!"];\n'
    for p in fd.propagators:
        style = stylize_connect(p)
        src += "edge [{}];\n".format(style)
        src += f"\t\t{p.source} -- {p.target};\n"
    rank_in = "{rank=min; "
    rank_out = "{rank=max; "

    for l in fd.legs:
        style = stylize_connect(l)
        if l.sense == "incoming":
            src += "edge [{}];\n".format(style)
            src += f"\t\t{l.id} -- {l.target};\n"
            rank_in += f"{l.id} "
        elif l.sense == "outgoing":
            src += "edge [{}];\n".format(style)
            src += f"\t\t{l.target} -- {l.id};\n"
            rank_out += f"{l.id} ;"
        else:
            # TODO maybe not error but just use the default
            raise Exception("Unknown sense")
    src += rank_in + "}\n"
    src += rank_out + "}\n"
    src += "}"
    return src


class DotRender(LatexRender):
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
        # super(Render,self).__init__(*args, fd=fd,**kwargs)
        self.preamble.append(Command("usepackage", NoEscape("tikz")))
        self.preamble.append(
            Command("usetikzlibrary", NoEscape("snakes,arrows,shapes"))
        )
        self.preamble.append(Command("usepackage", NoEscape("amsmath")))
        self.preamble.append(
            Command("usetikzlibrary", NoEscape("decorations.markings"))
        )
        if fd is not None:
            self.set_feynman_diagram(fd)

    def set_feynman_diagram(self, fd):
        super().set_feynman_diagram(fd)
        self.src_dot = feynman_to_dot(fd)
        self.set_src_diag(dot_to_tikz(self.src_dot))
        self.src_dot = self.src_dot.replace(REPLACE_THIS_WITH_A_BACKSLASH, "\\")

    def get_src_dot(self):
        return self.src_dot

    @staticmethod
    def valid_attribute( attr: str) -> bool:
        return super().valid_attribute(attr) or attr in ["x", "y", "label"]

    @staticmethod
    def valid_type( typ):
        if typ.lower() in map_feyn_to_tikz:
            return True
        return False
