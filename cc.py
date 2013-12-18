#!/usr/bin/python

import sys
import os.path
import getopt

__author__ = 'Jonathan Beaulieu'

instr = {"str1": "50", "str2": "70", "dis": "3c", "jmp": "23"}

def normalize_number(s, length=2):
    if s[0] == "0" and len(s) > 2:
        if s[1] == "b":
            n = int(s[2:], 2)
        elif s[1] == "x":
            n = int(s[2:], 16)
        else:
            n = int(s[1:], 8)
    else:
        n = int(s)
    return "0"*(length-len(hex(n)[2:])) + hex(n)[2:]


def compile_line(s):
    a = s.split()
    if len(a) == 0 or "#" == a[0][0]:
        return
    c = instr[a[0]]
    if "str" in a[0]:
        c = normalize_number(a[2]) + normalize_number(a[1], 4) + c
    elif a[0] == "dis":
        c = normalize_number(a[2]) + normalize_number(a[1]) + c
    elif a[0] == "jmp":
        c = normalize_number(a[1]) + c
    return c.lstrip("0")


def compile_lines(lines):
    doc = "v2.0 raw\n"
    print "dsf", len(lines)/8
    for row in xrange((len(lines)/8)+1):
        column_count = 0
        column = 0
        while column_count < 8:
            index = (row*8)+column
            if index >= len(lines):
                break
            compiled_line = compile_line(lines[index])
            if compiled_line:
                doc += compiled_line + " "
                column_count += 1
            column += 1
        doc += "\n"
    return doc


def main():
    input_filename = ""
    output_filename = "a.out"
    override = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["ifile=", "ofile=", "override"])
    except:
        print "cc.py -i <inputfile> [-o <outputfile>]"
        sys.exit(2)

    for opt, arg in opts:
        print opt, arg
        if opt in ("-i", "--ifile"):
            input_filename = arg
        elif opt in ("-o", "--ofile") and arg != "":
            output_filename = arg
        elif opt == "--override":
            override = True

    if not os.path.exists(input_filename):
        print "Input file does not exist."
        sys.exit(3)
    if os.path.exists(output_filename) and not override:
        answer = ""
        while answer != "y" and answer != "n":
            answer = raw_input("Do you want to replace output file (y)es or (n)o: ").lower()
        if answer == "n":
            sys.exit(3)

    lines = open(input_filename, "r").readlines()
    out = compile_lines(lines)
    open(output_filename, "w").write(out)

    print "Done."


if __name__ == '__main__':
    main()