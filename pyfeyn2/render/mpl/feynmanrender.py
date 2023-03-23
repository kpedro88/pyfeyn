from typing import List, Union

from feynman import Diagram
from matplotlib import pyplot as plt

from pyfeyn2.feynmandiagram import FeynmanDiagram, Leg, Propagator
from pyfeyn2.render.render import Render

namedlines = {
    "straight": [{"style": "simple"}],
    "gluon": [{"style": "loopy"}],
    "gluino": [
        {
            "style": "loopy",
        },
        {"style": "simple"},
    ],
    "photon": [{"style": "wiggly"}],
    "boson": [{"style": "wiggly"}],
    "ghost": [{"style": "dashed"}],
    "fermion": [{"style": "simple"}],
    "anti fermion": [{"style": "simple"}],
    "higgs": [{"style": "dashed"}],
    "gaugino": [
        {"style": "wiggly"},
        {"style": "simple"},
    ],
    "phantom": [],
}


def get_styled_lines(fd: FeynmanDiagram, p: Union[Propagator, Leg]) -> List[dict]:
    ret = []
    style = fd.get_style(p)
    for i in namedlines[style.getProperty("line").value]:
        d = {**i}
        if style.getProperty("arrow-sense") is not None:
            val = style.getProperty("arrow-sense").value
            if val != 0 and val != "none" and val != "None" and val != "0":
                d["arrow"] = True
                d["arrow_param"] = {"direction": float(val)}
                if style.getProperty("arrow-length") is not None:
                    d["arrow_param"]["length"] = float(
                        style.getProperty("arrow-length").value
                    )
                if style.getProperty("arrow-width") is not None:
                    d["arrow_param"]["width"] = float(
                        style.getProperty("arrow-width").value
                    )
                if style.getProperty("color") is not None:
                    d["arrow_param"]["color"] = style.getProperty("color").value
        else:
            d["arrow"] = False
        # copy css style to feynman kwargs dict
        for k in [
            "xamp",
            "yamp",
        ]:
            if style.getProperty(k) is not None:
                d[k] = float(style.getProperty(k).value)
        for k in ["nloops"]:
            if style.getProperty(k) is not None:
                d[k] = float(style.getProperty(k).value)
        for k in ["color"]:
            if style.getProperty(k) is not None:
                d[k] = style.getProperty(k).value
        ret.append(d)
    return ret


class FeynmanRender(Render):
    def __init__(self, fd=None, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=5.0,
        height=5.0,
        clean_up=True,
    ):
        buffer = 0.8
        # normaliuze to 1
        maxx = minx = maxy = miny = 0.0
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

        scalex = 1.0 / (maxx - minx) * buffer
        scaley = 1.0 / (maxy - miny) * buffer

        kickx = -minx + 1 / scalex * (1 - buffer) / 2.0
        kicky = -miny + 1 / scaley * (1 - buffer) / 2.0

        fig = plt.figure(figsize=(width, height))
        ax = fig.add_axes([0, 0, 1, 1], frameon=False)
        diagram = Diagram(ax)
        byid = {}
        for v in self.fd.vertices:
            byid[v.id] = diagram.vertex(
                xy=((v.x + kickx) * scalex, (v.y + kicky) * scaley)
            )
        for v in self.fd.legs:
            byid[v.id] = diagram.vertex(
                xy=((v.x + kickx) * scalex, (v.y + kicky) * scaley), marker=""
            )

        for p in self.fd.propagators:
            for style in get_styled_lines(self.fd, p):
                cur = diagram.line(byid[p.source], byid[p.target], **style)
            if p.label is not None:
                cur.text(p.label)
        for l in self.fd.legs:
            for style in get_styled_lines(self.fd, l):
                if l.sense[:2] == "in":
                    cur = diagram.line(byid[l.id], byid[l.target], **style)
                elif l.sense[:3] == "out":
                    cur = diagram.line(byid[l.target], byid[l.id], **style)
                else:
                    raise Exception("Unknown sense")
            if l.label is not None:
                cur.text(l.label)

        for l in self.fd.labels:
            diagram.text(
                l.x,
                l.y,
                l.text,
            )
        diagram.plot()
        if show:
            plt.show()
        if file is not None:
            plt.savefig(file)
        if clean_up:
            plt.close()
        return diagram

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return super(FeynmanRender, cls).valid_attributes() + [
            "x",
            "y",
            "label",
            "style",
        ]

    @classmethod
    def valid_types(cls) -> List[str]:
        return super(FeynmanRender, cls).valid_types() + list(namedlines.keys())

    @classmethod
    def valid_styles(cls) -> List[str]:
        return super(FeynmanRender, cls).valid_styles() + [
            "line",
            "color",
            "arrow-sense",
            "arrow-length",
            "arrow-width",
            "xamp",
            "yamp",
            "nloops",
        ]
