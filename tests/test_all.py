from matplotlib import pyplot as plt

import pyfeyn2
from pyfeyn2.render.all import AllRender


def test_renders():

    for prop in pyfeyn2.types:
        AllRender().demo_propagator(prop, show=False)
        plt.close()
