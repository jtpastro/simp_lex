#!/usr/bin/python3

import sys, getopt
from collections import defaultdict

class TEP:
	def __init__(self, filename):
		self.syn_group = {}
		self.syn_dict = defaultdict(list)
		with open(filename) as f:
			for entry in f:
				s_entry = entry.split()
				seq = int(s_entry[0][:-1])-1
				cat = s_entry[1][1:-1]
				synset = [word.strip(",") for word in s_entry[2:]]
				synset[0] = synset[0].strip("{")
				ant = -1
				if "<" in synset[-1]:
					ant += int(synset[-1].strip("<").strip(">"))
					synset = synset[:-1]
				synset[-1] = synset[-1].strip("}")
				for word in synset:
					self.syn_dict[word].append(seq)
				self.syn_group[seq] = (cat,synset,ant)
	
	def get_synonyms(self,word):
		return [self.syn_group[i][1] for i in self.syn_dict[word]]
	
	def get_antonyms(self,word):
		ant_list = []
		for i in self.syn_dict[word]:
			ant = self.syn_group[i][-1]
			if ant != -1:
				ant_list.append(self.syn_group[ant][1])
		return ant_list
	
	def get_class(self, word):
		return self.syn_group[self.syn_dict[word][0]][0]

def main(argv):
	_help = 'TEP.py -i <TEP2_file> -w <word>'
	inputfile = ''
	word = ''
	try:
		opts, args = getopt.getopt(argv,"hi:w:",["ifile=", "word="])
	except getopt.GetoptError:
		print (_help)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print (_help)
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-w", "--word"):
			word = arg
	if not inputfile:
		print("TEP2 file required.")
		print (_help)
		sys.exit(2)
	elif not word:
		print("Please provide a word with the argument -w.")
		print (_help)
		sys.exit(2)
	t = TEP(inputfile)
	syn = t.get_synonyms(word)
	if not syn:
		print ("This word is not present in the thesaurus.")
	else:
		for synset in syn:
			print (synset)
		
if __name__ == "__main__":
	main(sys.argv[1:])
