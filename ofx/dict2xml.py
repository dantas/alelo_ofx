from lxml import etree


def to_string(entry):
    return etree.tostring(entry, pretty_print=True)


def convert(parent, entry):
    if isinstance(parent, str):
        parent = etree.Element(parent)

    if isinstance(entry, dict):
        return _convert_dict(parent, entry)
    elif isinstance(entry, list):
        return _convert_list(parent, entry)
    elif etree.iselement(entry):
        parent.append(entry)
    else:
        parent.text = str(entry)


def _convert_dict(parent, dct):
    for key in dct:
        element = etree.SubElement(parent, key)
        value = dct[key]
        convert(element, value)
    return parent


def _convert_list(parent, lst):
    for x in lst:
        convert(parent, x)
    return parent
