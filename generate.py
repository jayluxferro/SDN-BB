#!/usr/bin/python

"""
Generate Results
"""
import sys
import logger as lg

def usage():
    lg.warning("Usage: {} [n1] [n2]\ne.g. {} S1 S2".format(sys.argv[0], sys.argv[0]))
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()

    # proceed as normal
