#!/usr/bin/env python3
"""
SSML (Speech Synthesis Markup Language) is a subset of XML specifically
designed for controlling synthesis. You can see examples of how the SSML
should be parsed in the unit tests below.
"""

#
# DO NOT USE CHATGPT, COPILOT, OR ANY AI CODING ASSISTANTS.
# Conventional auto-complete and Intellisense are allowed.
#
# DO NOT USE ANY PRE-EXISTING XML PARSERS FOR THIS TASK - lxml, ElementTree, etc.
# You may use online references to understand the SSML specification, but DO NOT read
# online references for implementing an XML/SSML parser.
#


from dataclasses import dataclass
from typing import List, Union, Dict
import xml.etree.ElementTree as ET

SSMLNode = Union["SSMLText", "SSMLTag"]


@dataclass
class SSMLTag:
    name: str
    attributes: dict[str, str]
    children: list[SSMLNode]

    def __init__(
        self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []
    ):
        self.name = name
        self.attributes = attributes
        self.children = children


@dataclass
class SSMLText:
    text: str

    def __init__(self, text: str):
        self.text = text


def parseSSML(ssml: str) -> SSMLNode:
    # TODO: implement this function
    def parse_element(elem:ET.Element)->SSMLNode:
        #children=list[SSMLNode]=[]
        children=[]
        if elem.text and elem.text.strip():
            children.append(SSMLText(elem.text))
        for child in elem:
            children.append(parse_element(child))
            if child.tail and child.tail.strip():
                children.append(SSMLText(child.tail))
        return SSMLTag(
            name=elem.tag,
            attributes=elem.attrib,
            children=children
        )
    root=ET.fromstring(ssml)
    return parse_element(root)
    #raise NotImplementedError()


def ssmlNodeToText(node: SSMLNode) -> str:
    # TODO: implement this function
    if isinstance(node,SSMLText):
        return node.text
    elif isinstance(node,SSMLTag):
        return ''.join(ssmlNodeToText(child) for child in node.children)
    else:
        return ''
    #raise NotImplementedError()


def unescapeXMLChars(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def escapeXMLChars(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

# Example usage:
ssml_string = '<speak>Hello, <break time="500ms"/>world!</speak>'
parsed_ssml = parseSSML(ssml_string)
text = ssmlNodeToText(parsed_ssml)
print(text)