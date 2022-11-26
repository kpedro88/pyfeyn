import dot2tex
from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic

from pyfeyn2.render.latex import LatexRender
from pyfeyn2.render.render import Render

map_feyn_to_tikz = {
    "photon": "snake",
    "gluon": "coil,aspect=0.3,segment length=1mm",
}


def dot_to_tikz(dot):
    return dot2tex.dot2tex(dot, format="tikz", figonly=True)


def feynman_to_dot(fd):
    src = "graph {"
    src += "rankdir=LR;"
    src += 'node [style="invis"];'
    for p in fd.propagators:
        src += 'edge [style="decorate,decoration={}"];\n'.format(
            map_feyn_to_tikz[p.type]
        )
        src += f"\t\t{p.source} -- {p.target};\n"
    rank_in = "{rank=min; "
    rank_out = "{rank=max; "

    for l in fd.legs:
        if l.sense == "incoming":
            src += 'edge [style="decorate,decoration={}"];\n'.format(
                map_feyn_to_tikz[p.type]
            )
            src += f"\t\t{l.id} -- {l.target};\n"
            rank_in += f"{l.id} "
        elif l.sense == "outgoing":
            src += 'edge [style="decorate,decoration={}"];\n'.format(
                map_feyn_to_tikz[p.type]
            )
            src += f"\t\t{l.target} -- {l.id};\n"
            rank_out += f"{l.id} ;"
        else:
            raise Exception("Unknown sense")
    src += rank_in + "}\n"
    src += rank_out + "}\n"
    src += "}"
    return src


class DotRender(LatexRender):
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
        # super(Render,self).__init__(*args, fd=fd,**kwargs)
        self.preamble.append(Command("usepackage", NoEscape("tikz")))
        self.preamble.append(
            Command("usetikzlibrary", NoEscape("snakes,arrows,shapes"))
        )
        self.preamble.append(Command("usepackage", NoEscape("amsmath")))
        self.append(NoEscape(dot_to_tikz(feynman_to_dot(fd))))
        self.src = self.dumps()
