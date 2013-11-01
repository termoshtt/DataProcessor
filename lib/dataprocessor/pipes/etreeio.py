#encoding:utf-8
import os.path


def read(filepath, root_path="."):
    """
    read xml file.

    This function return the etree and root element.
    You can specify root element by xpath.

    Examples
    --------

    >>> etree, root = read(xml_file_path, xpath)  # specify root by xpath
    >>> etree, root = read(xml_file_path)
    """
    import xml.etree.ElementTree as ET
    filepath = os.path.abspath(filepath)
    etree = ET.parse(filepath)
    return etree, etree.getroot().find(root_path)


def write(etree, filepath):
    etree.write(os.path.abspath(filepath), encoding="UTF-8")
    readable(filepath)


def readable(in_filepath, out_filepath=None):
    """
    modify xml file to be readable.

    Examples
    --------

    >>> readable(xml_file_path) # replace xml file with new readable xml file.
    >>> readable(xml_file_path, output_path)
    """
    if out_filepath is None:
        out_filepath = in_filepath
    in_filepath = os.path.abspath(in_filepath)
    out_filepath = os.path.abspath(out_filepath)
    f = open(in_filepath)
    string = f.read()
    f.close()

    string = _remove_indent(string)
    string = _split_tag(string)
    string = _add_newline(string)
    string = _indent(string)
    f = open(out_filepath, "w")
    f.write(string)
    f.close


def _remove_indent(string):
    import re
    sp = re.compile("[\n\r]")
    lines = sp.split(string)
    string = ""
    for line in lines:
        if line != "":
            string = string + line.strip() + "\n"
    return string


def _split_tag(string):
    import re
    reg1 = re.compile(r"<(.*?)>[ \t\b]*<(.*?)>")
    if reg1.search(string) is None:
        return string
    else:
        string = reg1.sub(r"<\1>\n<\2>", string, 1)
        return _split_tag(string)


def _add_newline(string):
    import re
    reg1 = re.compile(r"(</run>[ \t\b]*[\n\r])(\S+)")
    if reg1.search(string) is None:
        return string
    else:
        string = reg1.sub(r"\1\n\2", string, 1)
        return _add_newline(string)


def _check_tag(line):
    import re
    startend = re.compile("<.+?>.*?</.+?>")
    end = re.compile("</.+?>")
    onetag = re.compile("<.+?/>")
    start = re.compile("<.+?>")
    if startend.search(line):
        return "startend"
    elif onetag.search(line):
        return "oneline"
    elif end.search(line):
        return "end"
    elif start.search(line):
        return "start"
    else:
        return "none"


def _indent(string):
    import re
    sp = re.compile("[\n\r]")
    lines = sp.split(string)
    string = ""
    depth = 0
    for line in lines:
        if line == "":
            string = string + "\n"
        else:
            if _check_tag(line) == "start":
                string = string + "  " * (depth) + line + "\n"
                depth = depth + 1
            elif _check_tag(line) == "end":
                depth = depth - 1
                string = string + "  " * (depth) + line + "\n"
            else:
                string = string + "  " * (depth) + line + "\n"
    return string