#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :kGoSGFparser.py
 Author: FuGui
 Date: 2017/12/16-14:22
 Licence: 
 
'''
import os
from PyQt5.QtCore import QObject


class OffBoard(Exception): pass
class BadBoardSize(Exception): pass
class ParserFail(Exception): pass
class WrongNode(Exception): pass
class NoBoardSize(Exception): pass

def parse_sgf(sgf):
    print('parse_sgf -->:\n', sgf)
    sgf = sgf.strip()
    sgf = sgf.lstrip("(")       # the load_sgf_tree() function assumes the leading "(" has already been read and discarded

    root, __ = load_sgf_tree(sgf, None)
    return root


def load_sgf_tree(sgf, parent_of_local_root):   # The caller should ensure there is no leading "("

    root = None
    node = None

    inside = False      # Are we inside a value? i.e. in C[foo] the value is foo
    value = ""
    key = ""
    keycomplete = False
    chars_to_skip = 0

    print('load_sgf_tree -->\n', sgf)
    return None, 0
    print('load_sgf_tree --3333>\n')

    for i, c in enumerate(sgf):

        if chars_to_skip:
            chars_to_skip -= 1
            continue

        if inside:
            if c == "\\":               # Escape characters are saved
                value += "\\"
                try:
                    value += sgf[i + 1]
                except IndexError:
                    raise ParserFail
                chars_to_skip = 1
            elif c == "]":
                inside = False
                if node is None:
                    raise ParserFail
                node.add_value(key, value)
            else:
                value += c
        else:
            if c == "[":
                value = ""
                inside = True
                keycomplete = True
            elif c == "(":
                if node is None:
                    raise ParserFail
                __, chars_to_skip = load_sgf_tree(sgf[i + 1:], node)    # The child function will append the new tree to the node
            elif c == ")":
                if root is None:
                    raise ParserFail
                return root, i + 1          # return characters read
            elif c == ";":
                if node is None:
                    newnode = Node(parent = parent_of_local_root)
                    root = newnode
                    node = newnode
                else:
                    newnode = Node(parent = node)
                    node = newnode
            else:
                if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":   # Other chars are skipped, e.g. AddWhite becomes AW (saw this once)
                    if keycomplete:
                        key = ""
                        keycomplete = False
                    key += c

    if root is None:
        raise ParserFail

    return root, i + 1          # return characters read

def load(filename):

    with open(filename, encoding="utf8", errors="replace") as infile:
        contents = infile.read()

    # FileNotFoundError is just allowed to bubble up\
    root = parse_sgf(contents)

    # try:
    #     root = parse_sgf(contents)
    #
    # except ParserFail:      # All the parsers below can themselves raise ParserFail
    #
    #     if filename[-4:].lower() == ".gib":
    #         print("Parsing as SGF failed, trying to parse as GIB")
    #
    #         # These can be in variousdifferent encodings, I think,
    #         # so no attempt to switch to GBK or whatever...
    #
    #         # root = parse_gib(contents)
    #
    #     elif filename[-4:].lower() == ".ngf":
    #         print("Parsing as SGF failed, trying to parse as NGF")
    #
    #         # These seem to use GB18030:
    #
    #         with open(filename, encoding="gb18030", errors="replace") as infile:
    #             contents = infile.read()
    #
    #         # root = parse_ngf(contents)
    #
    #     elif filename[-4:].lower() in [".ugf", ".ugi"]:
    #         print("Parsing as SGF failed, trying to parse as UGF")
    #
    #         # These seem to usually be in Shift-JIS encoding, hence:
    #
    #         with open(filename, encoding="shift_jisx0213", errors="replace") as infile:
    #             contents = infile.read()
    #
    #         # root = parse_ugf(contents)
    #     else:
    #         raise

    # root.set_value("FF", 4)
    # root.set_value("GM", 1)
    # root.set_value("CA", "UTF-8")   # Force UTF-8
    #
    # if "SZ" in root.properties:
    #     size = int(root.properties["SZ"][0])
    # else:
    #     size = 19
    #     root.set_value("SZ", "19")
    #
    # if size > 19 or size < 1:
    #     raise BadBoardSize
    #
    # # The parsers just set up SGF keys and values in the nodes. We no longer update the boards
    # # when loading a file, but still need to update main line status and moves played:
    #
    # root.is_main_line = True
    # root.update_recursive(update_board = False)

    return root

def openFile(file):
    node = load(file)
    # print("node ", node)
    pass


if __name__ == '__main__':
    print(__file__ + __name__)
    pass