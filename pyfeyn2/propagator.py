from dataclasses import dataclass
from typing import Optional

from xml_dataclasses import xml_dataclass

from pyfeyn2 import io_utils

CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"


io_utils.print_as_xml(Propagator())
