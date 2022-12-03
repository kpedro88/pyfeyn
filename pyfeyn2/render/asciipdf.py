from pylatex import Command
from pylatex.utils import NoEscape, verbatim

from pyfeyn2.render.ascii import ASCIIRender
from pyfeyn2.render.latex import LatexRender


class ASCIIPDFRender(LatexRender, ASCIIRender):
    """Renders Feynman diagrams as ASCII art to PDF."""

    def __init__(self, fd, width=80, height=30, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)
        self.preamble.append(Command("usepackage", NoEscape("listings")))
        str = ASCIIRender.render(self, None, False, 100, width, height)
        self.set_src_diag("\\begin{lstlisting}" + str + "\\end{lstlisting}")
