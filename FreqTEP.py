#!/usr/bin/env python3

import sys, getopt
from collections import defaultdict
import bz2
from Synset import Synset
from CBFreq import CBFreq

class FreqTEP(Synset):
    def __init__(self, tepfile, cbfile):
        super(FreqTEP, self).__init__()
        freq_dict = CBFreq(cbfile).freq_dict
        with bz2.open(tepfile,"rt") as f:
            for entry in f:
                s_entry = entry.split("{")
                s_class = s_entry[0].split()
                seq = int(s_class[0][:-1])-1
                cat = s_class[1][1:-1]
                synset_str, antset = s_entry[1].split("}")
                synset = [word.strip(" ") for word in synset_str.split(",")]
                ant = -1
                if "<" in antset:
                    ant += int(antset.strip().strip("<").strip(">"))
                self.add_synset(seq, cat, ant)
                for word in synset:
                    self.add_word(word, seq, freq_dict[word])

def main(argv):
    _help = 'TEP.py -t <TEP2_file> -c CorpusBrasileiroFile -w <word>'
    tfile = ''
    cfile = ''
    word = ''
    try:
        opts, args = getopt.getopt(argv,"h:t:c:w:",["tfile=", 'cfile=', "word="])
    except getopt.GetoptError:
        print (_help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (_help)
            sys.exit()
        elif opt in ("-t", "--tfile"):
            tfile = arg
        elif opt in ("-c", "--cfile"):
            cfile = arg
        elif opt in ("-w", "--word"):
            word = arg
    if not tfile:
        print("TEP2 file required.")
        print (_help)
        sys.exit(2)
    elif not cfile:
        print("CorpusBrasileiro file required.")
        print (_help)
        sys.exit(2)
    elif not word:
        print("Please provide a word with the argument -w.")
        print (_help)
        sys.exit(2)
    t = FreqTEP(tfile, cfile)
    syn = t.get_synonyms(word)
    if not syn:
        print ("This word is not present in the thesaurus.")
    else:
        for synset in syn:
            print (synset)
		
if __name__ == "__main__":
    main(sys.argv[1:])

