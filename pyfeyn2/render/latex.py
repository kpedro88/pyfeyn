from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic

from pyfeyn2.render.render import Render


class LatexRender(Document, Render):
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
            documentclass=documentclass,
            document_options=document_options,
            **kwargs,
        )

    def get_src(self):
        return self.dumps()

    def render(self, file):
        return self.generate_pdf(file, clean_tex=True)
