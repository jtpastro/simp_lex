#!/usr/bin/python3

import sys, getopt
from collections import defaultdict, OrderedDict
from TEP import TEP


freq_dict = {}
with open("freq") as f:
    for entry in f:
        word, occur = entry.split()
        freq_dict[word] = int(occur)
t = TEP("base_tep2.txt")

def syn_freq(word):
    return (OrderedDict({(freq_dict[syn], syn) for syn in syn_set}) for syn_set in t.get_synonyms(word))

def most_freq_syn(word):
    most_freq = 0
    syn = word
    for i in syn_freq(word):
        for j in i:
            if j >= most_freq:
                most_freq = j
                syn = i[j]
    return syn

def main(argv):
    for i in argv:
        print(most_freq_syn(i))
	
if __name__ == "__main__":
    main(sys.argv[1:])

