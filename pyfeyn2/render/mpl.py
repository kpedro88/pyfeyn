import matplotlib.pyplot as plt
import numpy as np

from pyfeyn2.render.render import Render


def line(p1, p2, points=200):
    n = np.linspace(0, points, points)
    return (
        p1[0] + (p2[0] - p1[0]) * (n / points),
        p1[1] + (p2[1] - p1[1]) * (n / points),
    )


def spring(xp1, xp2, points=200, rot=3, amp=0.15, line_frac=0.2):
    p1 = [
        xp1[0] + (xp2[0] - xp1[0]) * line_frac,
        xp1[1] + (xp2[1] - xp1[1]) * line_frac,
    ]

    p2 = [
        xp2[0] - (xp2[0] - xp1[0]) * line_frac,
        xp2[1] - (xp2[1] - xp1[1]) * line_frac,
    ]

    n = np.linspace(0, points, points)
    alpha = np.arctan((p2[1] - p1[1]) / np.array([(p2[0] - p1[0])]))
    if p2[0] < p1[0]:
        alpha += np.pi
    w = rot / points * (2 * np.pi) + np.pi / points
    ret = (
        p1[0]
        + (p2[0] - p1[0]) * (n / points)
        + amp * (-np.cos(w * n - alpha) + np.cos(-alpha)),
        p1[1]
        + (p2[1] - p1[1]) * (n / points)
        + amp * (np.sin(w * n - alpha) - np.sin(-alpha)),
    )

    return (
        np.append(np.insert(ret[0], 0, xp1[0]), xp2[0]),
        np.append(np.insert(ret[1], 0, xp1[1]), xp2[1]),
    )


class MPLRender(Render):
    def __init__(self, fd, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def render(self, file=None, show=True):
        idtopos = {}
        for v in self.fd.vertices:
            idtopos[v.id] = (v.x, v.y)
        for l in self.fd.legs:
            idtopos[l.id] = (l.x, l.y)

        for p in self.fd.propagators:
            x, y = spring(idtopos[p.source], idtopos[p.target])
            plt.plot(x, y, "k-")
        for l in self.fd.legs:
            if l.sense == "incoming":
                x, y = spring(idtopos[l.id], idtopos[l.target])
                plt.plot(x, y, "k-")
            elif l.sense == "outgoing":
                x, y = spring(idtopos[l.target], idtopos[l.id])
                plt.plot(x, y, "k-")
            else:
                raise Exception("Unknown sense")

        if show:
            plt.show()
        if file is not None:
            plt.savefig(file)
