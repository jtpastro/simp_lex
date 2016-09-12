#!/usr/bin/env python3

import sys, getopt
from collections import defaultdict

class Synset:
    def __init__(self):
        self.syn_group = {}
        self.syn_dict = defaultdict(set)

    def add_synset(self, seq, cat, ant):
        self.syn_group[seq] = ({},cat, ant)

    def add_word(self, word, synset_seq, freq):
        self.syn_dict[word].add(synset_seq)
        self.syn_group[synset_seq][0][word] = freq
    
    def get_synonyms(self,word):
        for i in self.syn_dict[word]:
            yield self.syn_group[i][0]
    
    def get_antonyms(self,word):
        for i in self.syn_dict[word]:
            ant = self.syn_group[i][-1]
            if ant != -1:
                yield self.syn_group[ant][0]
    
    def get_class(self, word):
        for seq in self.syn_dict[word]:
            yield self.syn_group[seq][1]

