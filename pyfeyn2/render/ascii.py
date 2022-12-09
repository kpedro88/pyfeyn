from typing import List

from pyfeyn2.feynmandiagram import Point
from pyfeyn2.render.latex import LatexRender
from pyfeyn2.render.render import Render


class ASCIILine:
    def __init__(
        self,
        begin=" ",
        end=" ",
        vert=None,
        horz=None,
        left=None,
        up=None,
        right=None,
        down=None,
    ):
        self.begin = begin
        self.end = end

        if not isinstance(left, List):
            left = [left]
        self.left = left
        if not isinstance(up, List):
            up = [up]
        self.up = up
        if not isinstance(right, List):
            right = [right]
        self.right = right
        if not isinstance(down, List):
            down = [down]
        self.down = down

        if vert is not None:
            if not isinstance(vert, List):
                vert = [vert]
            self.down = vert
            self.up = vert
        if horz is not None:
            if not isinstance(horz, List):
                self.horz = [horz]
            self.right = horz
            self.left = horz
        self.index = 0

    def draw(self, pane, isrc, itar, scalex=1, scaley=1, kickx=0, kicky=0):
        width = len(pane[0])
        height = len(pane)
        # TODO normalize to width and height as well
        srcx = int((isrc.x + kickx) * scalex)
        srcy = int((isrc.y + kicky) * scaley)
        tarx = int((itar.x + kickx) * scalex)
        tary = int((itar.y + kicky) * scaley)

        if abs(srcx - tarx) > abs(srcy - tary):
            for i in range(srcx, tarx, 1 if srcx < tarx else -1):
                pane[round(srcy + (tary - srcy) * (i - srcx) / (-srcx + tarx))][i] = (
                    self.left[self.index % len(self.left)]
                    if srcx > tarx
                    else self.right[self.index % len(self.right)]
                )
                self.index += 1
        else:
            for i in range(srcy, tary, 1 if srcy < tary else -1):
                pane[i][round(srcx + (tarx - srcx) * (i - srcy) / (-srcy + tary))] = (
                    self.up[self.index % len(self.up)]
                    if srcy < tary
                    else self.down[self.index % len(self.down)]
                )

                self.index += 1
        # pane[tary][tarx] = self.vert[self.index % len(self.vert)]
        self.index += 1
        if self.begin is not None and self.begin != "":
            pane[srcy][srcx] = self.begin
        if self.end is not None and self.end != "":
            pane[tary][tarx] = self.end


class Gluon(ASCIILine):
    def __init__(self):
        super().__init__(begin="O", end="O", vert=["O"], horz=["O"])


class Photon(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", vert=["(", ")"], horz=["~"])


class Ghost(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", vert=["."], horz=["."])


class Fermion(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            left="--<--",
            right="-->--",
            up="||^||",
            down="||v||",
        )


class Scalar(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            left="..<..",
            right="..>..",
            up="::^::",
            down="::v::",
        )


class Ghost(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            vert=":",
            horz=".",
        )


class Higgs(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            vert="=",
            horz="H",
        )


namedlines = {
    "gluon": Gluon,
    "photon": Photon,
    "vector": Photon,
    "boson": Photon,
    "ghost": Ghost,
    "fermion": Fermion,
    "ghost": Ghost,
    "higgs": Higgs,
    "scalar": Scalar,
    "slepton": Scalar,
    "squark": Scalar,
}


class ASCIIRender(Render):
    """Renders Feynman diagrams to ASCII art."""

    def __init__(self, fd, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def render(self, file=None, show=True, resolution=100, width=None, height=None):
        maxx = minx = maxy = miny = 0
        for l in self.fd.legs:
            if l.x < minx:
                minx = l.x
            if l.x > maxx:
                maxx = l.x
            if l.y < miny:
                miny = l.y
            if l.y > maxy:
                maxy = l.y
        for l in self.fd.vertices:
            if l.x < minx:
                minx = l.x
            if l.x > maxx:
                maxx = l.x
            if l.y < miny:
                miny = l.y
            if l.y > maxy:
                maxy = l.y

        if width is None:
            width = int((maxx - minx + 1) * resolution / 100)
        if height is None:
            height = int((maxy - miny + 1) * resolution / 100)

        pane = []
        for i in range(height):
            pane.append([" "] * width)

        scalex = (width - 1) / (maxx - minx)
        scaley = (height - 1) / (maxy - miny)
        kickx = -minx
        kicky = -miny
        fmt = {"scalex": scalex, "kickx": kickx, "scaley": scaley, "kicky": kicky}

        for p in self.fd.propagators:
            src = self.fd.get_point(p.source)
            tar = self.fd.get_point(p.target)
            namedlines[p.type]().draw(pane, src, tar, **fmt)
        for l in self.fd.legs:
            tar = self.fd.get_point(l.target)
            if l.sense[:2] == "in" or l.sense[:8] == "anti-out":
                namedlines[l.type]().draw(pane, Point(l.x, l.y), tar, **fmt)
            elif l.sense[:3] == "out" or l.sense[:9] == "anti-in":
                namedlines[l.type]().draw(pane, tar, Point(l.x, l.y), **fmt)

        joined = "\n".join(["".join(row) for row in pane])
        if show:
            print(joined)
        return joined

    def valid_attribute(self, attr: str) -> bool:
        return super().valid_attribute(attr) or attr in ["x", "y"]

    def valid_type(self, typ: str) -> bool:
        if typ.lower() in namedlines:
            return True
        return False
