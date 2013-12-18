#!/usr/bin/python

import sys
import os.path
import getopt

__author__ = 'Jonathan Beaulieu'

instr = {"str1": "50", "str2": "70", "dis": "3c", "jmp": "23"}


def compile_line(s):
    a = s.split()
    c = instr[a[0]]
    if "str" in a[0]:
        c = a[2] + a[1] + c
    elif a[0] == "dis":
        c = a[2] + a[1] + c
    elif a[0] == "jmp":
        c = a[1] + c
    return c.lstrip("0")


def compile_lines(lines):
    doc = "v2.0 raw\n"
    print "dsf", len(lines)/8
    for row in xrange((len(lines)/8)+1):
        for column in xrange(8):
            index = (row*8)+column
            if index >= len(lines):
                continue
            doc += compile_line(lines[index]) + " "
        doc += "\n"
    return doc

a = ["str1 aba2 00",
"str2 0000 00",
"dis 07 00",
"jmp 00"
]

def main():
    input_filename = ""
    output_filename = "a.out"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["ifile=", "ofile="])
    except:
        print "cc.py -i <inputfile> [-o <outputfile>]"
        sys.exit(2)

    for opt, arg in opts:
        print opt, arg
        if opt in ("-i", "--ifile"):
            input_filename = arg
        elif opt in ("-o", "--ofile") and arg != "":
            output_filename = arg

    if not os.path.exists(input_filename):
        print "Input file does not exist."
        sys.exit(3)
    if os.path.exists(output_filename):
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