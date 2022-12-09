from pylatex import Command
from pylatex.utils import NoEscape, verbatim

from pyfeyn2.render.ascii import ASCIIRender
from pyfeyn2.render.latex import LatexRender


class ASCIIPDFRender(LatexRender, ASCIIRender):
    """Renders Feynman diagrams as ASCII art to PDF."""

    def __init__(self, fd, documentclass=None, docuement_options=None, *args, **kwargs):
        if documentclass is None:
            documentclass = "standalone"
        if docuement_options is None:
            docuement_options = ["preview", "crop"]
        super().__init__(
            fd,
            documentclass=documentclass,
            document_options=docuement_options,
            *args,
            **kwargs
        )
        self.preamble.append(Command("usepackage", NoEscape("listings")))

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        str = ASCIIRender.render(self, None, False, resolution, width, height)
        # str = str.replace("^", "\\^{}")
        # str = str.replace(">", "$>$")
        # str = str.replace("<", "$<$")
        self.set_src_diag("\\begin{lstlisting}" + str + "\\end{lstlisting}")
        super().render(file, show, resolution, width, height, clean_up)
