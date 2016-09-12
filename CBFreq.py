#!/usr/bin/env python3

import sys, getopt
from collections import defaultdict, OrderedDict
import bz2
import subprocess

class CBFreq:
    def __init__(self, filename):
        self.freq_dict = defaultdict(int)
        with open(filename,"rt") as f:
            while True:
                line1 = f.readline()
                if not line1:
                    break
                lemma, tags = line1.split('[')[1].split(']')
                lemma = lemma.split(',')
                cat = tags.split(',')[1]
                try:
                    freq = int(f.readline().split(',')[0])
                    if cat in ("adj", "n", "adv", "v-fin", "v-inf", "v-pcp") and lemma and lemma[0]:
                        for word in lemma:
                            self.freq_dict[word]+=freq
                except:
                    f.readline()

def main(argv):
    mfs = CBFreq("cbfreq_tagged.txt")
    print(mfs.freq_dict[argv[0]]) 

if __name__ == "__main__":
    main(sys.argv[1:])

