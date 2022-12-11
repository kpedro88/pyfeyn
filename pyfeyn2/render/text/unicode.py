from pylatexenc.latex2text import LatexNodes2Text

from pyfeyn2.render.text.ascii import ASCIIRender, Label


class ULabel(Label):
    def handle_tex(self, s):
        """
        Converts LaTeX to unicode.
        """
        ret = LatexNodes2Text().latex_to_text(s)
        return ret


class UnicodeRender(ASCIIRender):
    """Renders Feynman diagrams to Unicode art."""

    namedlines = {
        **ASCIIRender.namedlines,
        "label": ULabel,
    }
