#!/usr/bin/env python3

import sys, getopt
from collections import defaultdict, OrderedDict
from TEP import TEP
import bz2

class MFS:
    def __init__(self, tepfile, freqfile):
        self.freq_dict = defaultdict(int)
        with bz2.open(freqfile,"rt") as f:
            for entry in f:
                word, occur = entry.split()
                self.freq_dict[word] = int(occur)
        self.tep = TEP(tepfile)

    def syn_freq(self,word):
        return (OrderedDict({(self.freq_dict[syn], syn) for syn in syn_set}) for syn_set in self.tep.get_synonyms(word))

    def most_freq_syn(self,word):
        most_freq = 0
        syn = word
        for i in self.syn_freq(word):
            for j in i:
                if j >= most_freq:
                    most_freq = j
                    syn = i[j]
        return syn

def main(argv):
    mfs = MFS("base_tep2.txt.bz2", "freq.bz2")
    for i in argv:
        print(mfs.most_freq_syn(i))
	
if __name__ == "__main__":
    main(sys.argv[1:])

