"""Moved to :py:mod:`feynml`"""
from importlib.metadata import version

from feynml.connector import Connector
from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML as FeynML_
from feynml.feynml import Head, Meta, Tool
from feynml.leg import Leg
from feynml.momentum import Momentum
from feynml.pdgid import PDG
from feynml.point import Point
from feynml.propagator import Propagator
from feynml.style import Styled
from feynml.vertex import Vertex


class FeynML(FeynML_):
    """FeynML with pyfeyn2 meta tag."""

    def __post_init__(self):
        self.head.metas.append(Meta("pyfeyn2", version("pyfeyn2")))
        return super().__post_init__()
