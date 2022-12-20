from matplotlib import pyplot as plt

from pyfeyn2.render.all import AllRender


def test_renders():
    for prop in AllRender.valid_types():
        AllRender().demo_propagator(prop, show=False)
        plt.close()
