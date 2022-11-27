import pyx
from IPython.display import display
from pyx import *
from wand.image import Image as WImage

# from pyfeyn2.feynmandiagram import Line, Point
from pyfeyn2.render.pyx.deco import Arrow, PointLabel
from pyfeyn2.render.pyx.diagrams import FeynDiagram
from pyfeyn2.render.pyx.lines import Line, NamedLine
from pyfeyn2.render.pyx.points import (
    SQUARE,
    CircleMark,
    DecoratedPoint,
    NamedMark,
    Point,
    SquareMark,
)
from pyfeyn2.render.render import Render


class PyxRender(Render):
    def __init__(self, fd, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def render(self, file=None, show=True, resolution=100, width=None, height=None):
        pyxfd = FeynDiagram()
        for v in self.fd.vertices:
            dp = DecoratedPoint(v.x, v.y)
            dp = self.apply_layout(v.style, dp)
            if v.label is not None:
                dp.setFillstyles(PointLabel(dp, v.label, displace=3, angle=90))
            pyxfd.add(dp)
        for l in self.fd.legs:
            tar = self.fd.get_point(l.target)
            if l.sense[:2] == "in" or l.sense[:8] == "anti-out":
                nl = NamedLine[l.type](Point(l.x, l.y), Point(tar.x, tar.y))
            elif l.sense[:3] == "out" or l.sense[:9] == "anti-in":
                nl = NamedLine[l.type](Point(tar.x, tar.y), Point(l.x, l.y))
            nl = nl.bend(l.bend)
            nl = self.apply_layout(v.style, nl)
            nl = nl.addLabel(l.label)

        for p in self.fd.propagators:
            src = self.fd.get_point(p.source)
            tar = self.fd.get_point(p.target)
            nl = NamedLine[p.type](Point(src.x, src.y), Point(tar.x, tar.y))
            nl = nl.bend(p.bend)
            nl = self.apply_layout(v.style, nl)
            nl = nl.addLabel(l.label)
        pyxfd.draw(file)
        wi = WImage(filename=file, resolution=resolution, width=width, height=height)
        if show:
            display(wi)
        return wi

    def apply_layout(self, stylestring, obj):
        """Apply the decorators encoded in a style string to an object."""
        if stylestring is None:
            return obj
        styleelements = stylestring.split(";")
        styledict = {}
        for styling in styleelements:
            if styling == "":
                break
            s = styling.split(":")
            styledict[s[0].lstrip().rstrip()] = s[1]
        if "fill-style" in styledict:
            filltype = styledict["fill-style"].split()
            if filltype[0] == "solid":
                R, G, B = [
                    eval("0x%s" % x) / 255.0
                    for x in [filltype[1][n : n + 2] for n in (1, 3, 5)]
                ]
                obj.fillstyles = [pyx.color.rgb(R, G, B)]
            elif filltype[0] == "hatched":
                D, A = float(filltype[1]), int(filltype[2])
                obj.fillstyles = [pyx.pattern.hatched(D, A)]
            elif filltype[0] == "crosshatched":
                D, A = float(filltype[1]), int(filltype[2])
                obj.fillstyles = [pyx.pattern.crosshatched(D, A)]
        if ("mark-shape" in styledict or "mark-size" in styledict) and isinstance(
            obj, DecoratedPoint
        ):
            try:
                marktype = NamedMark[styledict["mark-shape"]]
            except:
                marktype = SQUARE
            try:
                marksize = float(styledict["mark-size"])
            except:
                marksize = 0.075
            obj.setMark(marktype(size=marksize))
        if (
            "arrow-size" in styledict
            or "arrow-angle" in styledict
            or "arrow-constrict" in styledict
            or "arrow-pos" in styledict
        ) and isinstance(obj, Line):
            try:
                arrsize = pyx.unit.length(float(styledict["arrow-size"]), unit="cm")
            except:
                arrsize = 6 * pyx.unit.v_pt
            try:
                arrangle = float(styledict["arrow-angle"])
            except:
                arrangle = 45
            try:
                arrconstrict = float(styledict["arrow-constrict"])
            except:
                arrconstrict = 0.8
            try:
                arrpos = float(styledict["arrow-pos"])
            except:
                arrpos = 0.5
            obj.addArrow(arrow=Arrow(arrpos, arrsize, arrangle, arrconstrict))
        if (
            "parallel-arrow-size" in styledict
            or "parallel-arrow-angle" in styledict
            or "parallel-arrow-constrict" in styledict
            or "parallel-arrow-pos" in styledict
            or "parallel-arrow-length" in styledict
            or "parallel-arrow-displace" in styledict
            or "parallel-arrow-sense" in styledict
        ) and isinstance(obj, Line):
            try:
                arrsize = pyx.unit.length(
                    float(styledict["parallel-arrow-size"]), unit="cm"
                )
            except:
                arrsize = 6 * pyx.unit.v_pt
            try:
                arrangle = float(styledict["parallel-arrow-angle"])
            except:
                arrangle = 45
            try:
                arrconstrict = float(styledict["parallel-arrow-constrict"])
            except:
                arrconstrict = 0.8
            try:
                arrpos = float(styledict["parallel-arrow-pos"])
            except:
                arrpos = 0.5
            try:
                arrlen = float(styledict["parallel-arrow-length"])
            except:
                arrlen = 0.5 * pyx.unit.v_cm
            try:
                arrdisp = float(styledict["parallel-arrow-displace"])
            except:
                arrdisp = 0.3
            try:
                arrsense = int(styledict["parallel-arrow-sense"])
            except:
                arrsense = +1
            obj.addParallelArrow(
                arrpos, arrdisp, arrlen, arrsize, arrangle, arrconstrict, arrsense
            )
        if "is3d" in styledict and isinstance(obj, Line):
            fwords = ["0", "no", "false", "f", "off"]
            twords = ["1", "yes", "true", "t", "on"]
            if styledict["is3d"].lstrip().lower() in fwords:
                obj.set3D(False)
            elif styledict["is3d"].lstrip().lower() in twords:
                obj.set3D(True)
        return obj
