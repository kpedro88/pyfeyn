import copy

import dot2tex
from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.render.latex import LatexRender
from pyfeyn2.render.render import Render

# https://tikz.dev/tikz-decorations
map_feyn_to_tikz = {
    "vector": "decorate,decoration=snake",
    "boson": "decorate,decoration=snake",
    "photon": "decorate,decoration=snake",
    "gluon": "decorate,decoration=coil,aspect=0.3,segment length=1mm",
    "ghost": "dotted",
    "fermion": "->.",
    "higgs": "densely dashed",
    "scalar": "densely dashed",
    "slepton": "densely dashed",
    "squark": "densely dashed",
}


def feynman_adjust_points(feyndiag, size=5):
    # deepcopy
    fd = copy.deepcopy(feyndiag)
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
    return dot2tex.dot2tex(dot, format="tikz", figonly=True)


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
    for p in fd.propagators:
        src += 'edge [style="{}"];\n'.format(map_feyn_to_tikz[p.type])
        src += f"\t\t{p.source} -- {p.target};\n"
    rank_in = "{rank=min; "
    rank_out = "{rank=max; "

    for l in fd.legs:
        if l.sense == "incoming":
            src += 'edge [style="{}"];\n'.format(map_feyn_to_tikz[l.type])
            src += f"\t\t{l.id} -- {l.target};\n"
            rank_in += f"{l.id} "
        elif l.sense == "outgoing":
            src += 'edge [style="{}"];\n'.format(map_feyn_to_tikz[l.type])
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
        if fd is not None:
            self.set_feynman_diagram(fd)

    def set_feynman_diagram(self, fd):
        super().set_feynman_diagram(fd)
        self.src_dot = feynman_to_dot(fd)
        self.set_src_diag(dot_to_tikz(self.src_dot))

    def get_src_dot(self):
        return self.src_dot

    def valid_attribute(self, attr: str) -> bool:
        return super().valid_attribute(attr) or attr in ["x", "y"]

    def valid_type(self, typ):
        if typ.lower() in map_feyn_to_tikz:
            return True
        return False
