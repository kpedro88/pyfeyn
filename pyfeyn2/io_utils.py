from xml.dom.minidom import parseString

from dicttoxml import dicttoxml
from xml_marshaller import xml_marshaller


def print_as_xml(obj):
    # print(parseString(dicttoxml(vars(obj),attr_type=False)).toprettyxml())
    # print()
    # print(parseString(dicttoxml(vars(obj),attr_type=True)).toprettyxml())
    # print()
    print(parseString(xml_marshaller.dumps(obj)).toprettyxml())
