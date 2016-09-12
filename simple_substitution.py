#!/usr/bin/env python3

import sys, getopt
import pickle
from FreqTEP import FreqTEP

def main():
    with open('FreqTEP.pickle', 'rb') as f:
        freqtep = pickle.load(f)
        line_no, total, subs = 0,0,0
        for line in sys.stdin:
            line_no += 1
            for word in line.split():
                total += 1
                best_syn = word
                freq = 0
                for synset in freqtep.get_synonyms(word):
                    for syn in synset:
                        if synset[syn] > freq:
                            best_syn = syn
                if best_syn != word:
                    subs += 1
                    print(line_no, ":", word, "->", syn)
        print("number of words:", total)
        print("number of substitutions:", subs, str(subs/total*100)+"%")
	
if __name__ == "__main__":
    main()

