import shutil
import tempfile
import traceback

from matplotlib import pyplot as plt
from pylatex import Figure, NoEscape, SubFigure

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
        document_options=None,
        *args,
        **kwargs,
    ):
        if document_options is None:
            document_options = ["varwidth"]
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

        try:
            if not subfigure:
                print("Pyx:")
            PyxRender(fd).render(dirpath + "/pyx.pdf", **dynarg)
        except Exception as e:
            print("Pyx failed:")
            print(traceback.format_exc())

        try:
            if not subfigure:
                print("Tikz:")
            TikzFeynmanRender(fd).render(dirpath + "/tikz.pdf", **dynarg)
        except Exception as e:
            print("Tikz failed:")
            print(traceback.format_exc())

        try:
            if not subfigure:
                print("Feynmp:")
            FeynmpRender(fd).render(dirpath + "/feynmp.pdf", **dynarg)
        except Exception as e:
            print("Feynmp failed:", e)
            print(traceback.format_exc())

        try:
            if not subfigure:
                print("Dot:")
            DotRender(fd).render(dirpath + "/dot.pdf", **dynarg)
        except Exception as e:
            print("Dot failed:", e)
            print(traceback.format_exc())

        try:
            if not subfigure:
                print("ASCIIPDF:")
            ASCIIPDFRender(fd).render(dirpath + "/asciipdf.pdf", **dynarg)
        except Exception as e:
            print("ASCIIPDF failed:", e)
            print(traceback.format_exc())

        try:
            if not subfigure:
                print("MPL:")
            MPLRender(fd).render(dirpath + "/mpl.pdf", **dynarg)
            plt.close()
        except Exception as e:
            print("MPL failed:", e)
            print(traceback.format_exc())

        with self.create(Figure(position="h!")):

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

    def valid_style(self, style: str) -> bool:
        return True in [r.valid_style(style) for r in renderers]

    def valid_attribute(self, attr: str) -> bool:
        return True in [r.valid_attribute(attr) for r in renderers]

    def valid_type(self, typ: str) -> bool:
        return True in [r.valid_type(typ) for r in renderers]


renderers = [
    PyxRender(),
    TikzFeynmanRender(),
    FeynmpRender(),
    DotRender(),
    ASCIIPDFRender(),
    MPLRender(),
]
