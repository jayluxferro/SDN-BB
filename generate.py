#!/usr/bin/python

"""
Generate Results
"""
import sys
import logger as lg
import helper as hp

def usage():
    lg.warning("Usage: {} [n1] [n2] [iperf commands]\ne.g. {} s1 s2 -s".format(sys.argv[0], sys.argv[0]))
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()

    # proceed as normal
    n1 = sys.argv[1].strip().lower()
    n2 = sys.argv[2].strip().lower()
    params = sys.argv[3:]

    isServer = False
    # check to see if tcp or udp
    try:
        params.index('-u')
        isTCP = False
    except:
        isTCP = True

    try:
        params.index('-s')
        isServer = True
        hp.server(n1, n2, params, isTCP)
    except:
        # not a server
        pass

    # checking which proto to run
    if isServer == False:
        lg.default("Running simulation for {} <=> {}".format(n1, n2))
        if isTCP == True:
            hp.iperf_tcp(n1, n2, params)
        else:
            hp.iperf_udp(n1, n2, params)
