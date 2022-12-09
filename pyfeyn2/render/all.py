import copy
import shutil
import tempfile

from matplotlib import pyplot as plt
from pylatex import Document, Figure, NoEscape, Section, SubFigure

from pyfeyn2.render.asciipdf import ASCIIPDFRender
from pyfeyn2.render.dot import DotRender
from pyfeyn2.render.feynmp import FeynmpRender
from pyfeyn2.render.latex import LatexRender
from pyfeyn2.render.mpl import MPLRender
from pyfeyn2.render.pyx.pyxrender import PyxRender
from pyfeyn2.render.tikzfeynman import TikzFeynmanRender


class AllRender(LatexRender):
    """Render all diagrams to PDF."""

    def __init__(
        self,
        fd=None,
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
        subfigure=False,
        resolution=None,
        width=None,
        height=None,
    ):
        fd = self.fd
        self.dirpath = tempfile.mkdtemp()
        dirpath = self.dirpath

        dynarg = {}
        if show and not subfigure:
            dynarg["show"] = True
            if resolution is not None:
                dynarg["resolution"] = resolution
            if width is not None:
                dynarg["width"] = width
            if height is not None:
                dynarg["height"] = height
        else:
            dynarg = {"show": False}

        if not subfigure:
            print("Pyx:")
        PyxRender(fd).render(dirpath + "/pyx.pdf", **dynarg)
        if not subfigure:
            print("Tikz:")
        TikzFeynmanRender(fd).render(dirpath + "/tikz.pdf", **dynarg)
        if not subfigure:
            print("Feynmp:")
        FeynmpRender(fd).render(dirpath + "/feynmp.pdf", **dynarg)
        if not subfigure:
            print("Dot:")
        DotRender(fd).render(dirpath + "/dot.pdf", **dynarg)
        if not subfigure:
            print("ASCIIPDF:")
        ASCIIPDFRender(fd).render(dirpath + "/asciipdf.pdf", **dynarg)
        if not subfigure:
            print("MPL:")
        MPLRender(fd).render(dirpath + "/mpl.pdf", **dynarg)
        plt.close()

        with self.create(Figure(position="h!")) as kittens:

            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/pyx.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("Tikz")
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/tikz.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("Tikz")
            self.append(NoEscape(r"\\"))
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/feynmp.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("FeynMP")
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/dot.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("Dot")
            self.append(NoEscape(r"\\"))
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/asciipdf.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("ASCIIPDF")
            with self.create(SubFigure(position="b")) as subfig:
                subfig.add_image(
                    dirpath + "/mpl.pdf", width=NoEscape("0.49\\textwidth")
                )
                subfig.add_caption("MPL")
        if subfigure:
            super().render(file, show, resolution, width, height)
        shutil.rmtree(self.dirpath)
