from typing import List

from pyfeyn2.feynmandiagram import Point
from pyfeyn2.render.ascii import ASCIIRender
from pyfeyn2.render.latex import LatexRender
from pyfeyn2.render.render import Render


class ASCIIPDFRender(ASCIIRender, LatexRender):
    """Renders Feynman diagrams as ASCII art to PDF."""

    def __init__(self, fd, width=100, height=20, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)
        str = ASCIIRender.render(self, None, False, 100, width, height)
        self.set_src_diag(str)
