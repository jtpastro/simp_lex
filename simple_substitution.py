#!/usr/bin/env python3

import sys, getopt
from collections import defaultdict, OrderedDict
from most_freq_syn import MFS

def main():
    mfs = MFS("base_tep2.txt.bz2", "freq.bz2")
    line_no, total, subs = 0,0,0
    for line in sys.stdin:
        line_no += 1
        for word in line.split():
            total += 1
            syn = mfs.most_freq_syn(word)
            if syn != word:
                subs += 1
                print(line_no, ":", word, "->", syn)
    print("number of words:", total)
    print("number of substitutions:", subs, str(subs/total*100)+"%")
	
if __name__ == "__main__":
    main()

