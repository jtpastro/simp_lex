#!/usr/bin/python3

import sys, getopt
from collections import defaultdict, OrderedDict
from MFS import MFS



def main(argv):
    mfs = MFS("base_tep2.txt", "freq")
    for i in argv:
        print(mfs.most_freq_syn(i))
	
if __name__ == "__main__":
    main(sys.argv[1:])

