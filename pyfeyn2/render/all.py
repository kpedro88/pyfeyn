import copy
import shutil
import tempfile

from matplotlib import pyplot as plt
from pylatex import Document, Figure, NoEscape, Section, SubFigure

from pyfeyn2.render.asciipdf import ASCIIPDFRender
from pyfeyn2.render.dot import DotRender
from pyfeyn2.render.latex import LatexRender
from pyfeyn2.render.mpl import MPLRender
from pyfeyn2.render.tikzfeynman import TikzFeynmanRender


class AllRender(LatexRender):
    """Render all diagrams to PDF."""

    def __init__(
        self,
        fd,
        documentclass="standalone",
        document_options=["varwidth"],
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

    def render(
        self,
        file=None,
        show=True,
        subfigure=True,
        resolution=100,
        width=None,
        height=None,
    ):
        fd = self.fd
        self.dirpath = tempfile.mkdtemp()
        dirpath = self.dirpath
        if show and not subfigure:
            dynarg = {
                "show": True,
                "resolution": resolution,
                "width": width,
                "height": height,
            }
        else:
            dynarg = {"show": False}
        ASCIIPDFRender(fd).render(dirpath + "/asciipdf.pdf", **dynarg)
        TikzFeynmanRender(fd).render(dirpath + "/tikz.pdf", **dynarg)
        DotRender(fd).render(dirpath + "/dot.pdf", **dynarg)
        MPLRender(fd).render(dirpath + "/mpl.pdf", **dynarg)
        plt.close()
        with self.create(Figure(position="h!")) as kittens:
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/asciipdf.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("ASCIIPDF")
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/tikz.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("Tikz")
            self.append(NoEscape(r"\\"))
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/dot.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("Dot")
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/mpl.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("MPL")
        if subfigure:
            super().render(file, show, resolution, width, height)
        shutil.rmtree(self.dirpath)
