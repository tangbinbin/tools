#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import getopt
import datetime
import time

def main(args):
    try:
        opts, other = getopt.getopt(args, "hi:o:", ["help"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    infile = outfile = ""
    for k, v in opts:
        if k in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif k == "-i":
            infile = v
        elif k == "-o":
            outfile = v
        else:
            print "unknown options"
            sys.exit(3)
    read_file(infile, outfile)

def usage():
    sl = [
            "general_log_parse.py usage:",
            "-h, --help: print help message",
            "-i: input file", 
            "-o: output file"
         ]
    print "\n    ".join(sl)
    print "\nexample:"
    print "    ./general_log_parse.py -i a.log -o b.log"

def read_file(infile, outfile):
    if infile == "" or outfile == "":
        print "infile or outfile unknown"
        usage()
        sys.exit(1)
    fo = open(infile, "r+")
    fw = open(outfile, "w+")
    buf = ""
    try:
        for line in fo:
            ws, tmp = parse(line, buf)
            if ws == "":
                buf = tmp
            else:
                fw.write(ws)
                buf = tmp
    finally:
        print "read over"
    fo.close()
    fw.close()

def parse(line, buf):
    sl = line.split("\t")
    l = len(sl)
    if l == 1:
        if buf == "":
            return "", ""
        return "", buf.replace("\n", " ") + line
    elif has_bad(line):
        return buf, ""
    elif has_qoe(line):
        if l == 4:
            if has_qoe(sl[2]):
                return buf, sl[3]
            elif has_qoe(sl[1]):
                return buf, " ".join(sl[2:])
            else:
                pass
        elif l == 3:
            return buf, sl[2]
        else:
            if has_qoe(sl[2]):
                return buf, " ".join(sl[3:])
            elif has_qoe(sl[1]):
                return buf, " ".join(sl[2:])
            else:
                pass
    else:
        return "", buf.replace("\n", " ") + line

def has_qoe(s):
    if s.find("Query") >=0:
        return True
    elif s.find("Execute") >= 0:
        return True
    else:
        return False

def has_bad(line):
    if line.find("Quit") >=0:
        return True
    elif line.find("Connect") >=0:
        return True
    elif line.find("Prepare") >=0:
        return True
    elif line.find("Close stmt") >=0:
        return True
    elif line.find("Init DB") >=0:
        return True
    elif line.find("Id\tCommand") >=0:
        return True
    else:
        return False

if __name__ == '__main__':
    ''' '''
    main(sys.argv[1:])
