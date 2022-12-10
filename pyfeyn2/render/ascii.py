import copy
import re
from typing import Iterable, List

from pyfeyn2.feynmandiagram import Point
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

        if not isinstance(left, Iterable):
            left = [left]
        self.left = left
        if not isinstance(up, Iterable):
            up = [up]
        self.up = up
        if not isinstance(right, Iterable):
            right = [right]
        self.right = right
        if not isinstance(down, Iterable):
            down = [down]
        self.down = down

        if vert is not None:
            if not isinstance(vert, Iterable):
                vert = [vert]
            self.down = vert
            self.up = vert
        if horz is not None:
            if not isinstance(horz, Iterable):
                self.horz = [horz]
            self.right = horz
            self.left = horz
        self.index = 0

    def inc_index(self) -> bool:
        self.index += 1
        return True

    def draw(self, pane, isrc, itar, scalex=1, scaley=1, kickx=0, kicky=0):
        # width = len(pane[0])
        # height = len(pane)
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
                if not self.inc_index():
                    return
        else:
            for i in range(srcy, tary, 1 if srcy < tary else -1):
                pane[i][round(srcx + (tarx - srcx) * (i - srcy) / (-srcy + tary))] = (
                    self.down[self.index % len(self.up)]
                    if srcy < tary
                    else self.up[self.index % len(self.down)]
                )
                if not self.inc_index():
                    return
        # pane[tary][tarx] = self.vert[self.index % len(self.vert)]

        if not self.inc_index():
            return
        if self.begin is not None and self.begin != "":
            pane[srcy][srcx] = self.begin
        if self.end is not None and self.end != "":
            pane[tary][tarx] = self.end


class Gluon(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", vert=["O"], horz=["O"])


class Photon(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", vert=["(", ")"], horz=["~"])


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


class Gluino(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", vert=["&"], horz=["&"])


class Gaugino(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", vert=["$"], horz=["$"])


def remove_tex(s):
    s = s.replace("\\bar", "_")
    s = s.replace("\\tilde", "~")
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    return (
        s.replace("$", "")
        .replace("{", "")
        .replace("}", "")
        .replace("\\(", "")
        .replace("\\)", "")
        .replace("\\", "")
        .replace("^", "")
    )


class Label(ASCIILine):
    def __init__(self, label, rm_tex=True):
        if rm_tex:
            self.label = remove_tex(label)
        else:
            self.label = label
        super().__init__(begin=None, end=None, vert=self.label, horz=self.label)

    def inc_index(self) -> bool:
        ret = super().inc_index()
        if self.index > len(self.label) - 1:
            return False
        return ret

    def draw(self, pane, isrc, itar, scalex=1, scaley=1, kickx=0, kicky=0):
        jsrc = copy.copy(isrc)
        jtar = copy.copy(itar)

        # reduce length to 1/3 in the middle
        jsrc.x = (itar.x - isrc.x) / 3.0 + isrc.x
        jsrc.y = (itar.y - isrc.y) / 3.0 + isrc.y
        jtar.x = (itar.x - isrc.x) / 3.0 * 2.0 + isrc.x
        jtar.y = (itar.y - isrc.y) / 3.0 * 2.0 + isrc.y

        ## shift the line
        shift = 3.0
        # horizonral
        if abs(isrc.x - itar.x) > abs(isrc.y - itar.y):
            # left to right -> shift up
            if isrc.x < itar.x:
                jsrc.y -= shift / scaley
                jtar.y -= shift / scaley
            # right to left -> shift down
            else:
                jsrc.y += shift / scaley
                jtar.y += shift / scaley

        # vertical
        else:
            # up to down -> shift left
            if isrc.y < itar.y:
                jsrc.x -= shift / scalex
                jtar.x -= shift / scalex
            # down to up -> shift right
            else:
                jsrc.x += shift / scalex
                jtar.x += shift / scalex

        super().draw(pane, jsrc, jtar, scalex, scaley, kickx, kicky)
        self.index = 0


class Phantom(ASCIILine):
    def __init__(self):
        super().__init__(begin=None, end=None, vert="", horz="")

    def draw(self, pane, isrc, itar, scalex=1, scaley=1, kickx=0, kicky=0):
        pass


namedlines = {
    "gluon": Gluon(),
    "photon": Photon(),
    "vector": Photon(),
    "boson": Photon(),
    "fermion": Fermion(),
    "ghost": Ghost(),
    "higgs": Higgs(),
    "scalar": Scalar(),
    "slepton": Scalar(),
    "squark": Scalar(),
    "gluino": Gluino(),
    "gaugino": Gaugino(),
    "phantom": Phantom(),
}


class ASCIIRender(Render):
    """Renders Feynman diagrams to ASCII art."""

    def __init__(self, fd=None, *args, **kwargs):
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

        shift = 2
        # maxx = maxx + shift
        maxy = maxy + shift
        # minx = minx - shift
        miny = miny - shift

        if width is None:
            width = int((maxx - minx) * resolution / 10)
        if height is None:
            height = int(
                (maxy - miny) * resolution / 10 / 2
            )  # divide by two to make it look better due to aspect ratio

        pane = []
        for _ in range(height):
            pane.append([" "] * width)

        scalex = (width - 1) / (maxx - minx)
        scaley = -(height - 1) / (maxy - miny)
        kickx = -minx
        kicky = -maxy
        fmt = {"scalex": scalex, "kickx": kickx, "scaley": scaley, "kicky": kicky}

        for p in self.fd.propagators:
            src = self.fd.get_point(p.source)
            tar = self.fd.get_point(p.target)
            namedlines[p.type].draw(pane, src, tar, **fmt)
            if p.label is not None:
                Label(p.label).draw(pane, src, tar, **fmt)
        for l in self.fd.legs:
            tar = self.fd.get_point(l.target)
            if l.sense[:2] == "in" or l.sense[:8] == "anti-out":
                namedlines[l.type].draw(pane, Point(l.x, l.y), tar, **fmt)
                if l.label is not None:
                    Label(l.label).draw(pane, Point(l.x, l.y), tar, **fmt)
            elif l.sense[:3] == "out" or l.sense[:9] == "anti-in":
                namedlines[l.type].draw(pane, tar, Point(l.x, l.y), **fmt)
                if l.label is not None:
                    Label(l.label).draw(pane, tar, Point(l.x, l.y), **fmt)

        joined = "\n".join(["".join(row) for row in pane])
        if show:
            print(joined)
        return joined

    def valid_attribute(self, attr: str) -> bool:
        return super().valid_attribute(attr) or attr in ["x", "y", "label"]

    def valid_type(self, typ: str) -> bool:
        if typ.lower() in namedlines:
            return True
        return False
