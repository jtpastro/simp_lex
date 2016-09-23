#!/usr/bin/env python3

class POSTaggedWord:
    catset = {'ADJ', 'ADV', 'DET', 'EC', 'IN', 'KC', 'KS', 'N', 'NUM', 'PERS', 'PROP', 'PRP','SPEC','V'}
    tagset = {'Case': {'DAT', 'NOM/PIV', 'NOM', 'ACC', 'PIV', 'ACC/DAT'}, 'Tense': {'COND', 'FUT', 'MQP', 'PR', 'PS', 'IMPF'}, 'Gender': {'F', 'M', 'M/F'}, 'Person': {'1', '1S', '1P', '0/1/3S', '2S', '3P', '1/3S', '2', '3', '2P', '3S'}, 'Number': {'S', 'P', 'S/P'}, 'Finiteness': {'INF', 'VFIN', 'GER', 'PCP'}, 'Mood': {'SUBJ', 'IND', 'IMP'}}
    require_tag = {'N': {'Gender', 'Number'}, 'NUM': {'Gender', 'Number'}, 'PROP': {'Gender', 'Number'}, 'VFIN': {'Tense', 'Mood', 'Number', 'Person'}, 'PERS': {'Case', 'Gender', 'Number', 'Person'}, 'SPEC': {'Gender', 'Number'}, 'ADJ': {'Gender', 'Number'}, 'PCP': {'Gender', 'Number'}, 'INF': {'Number', 'Person'}, 'DET': {'Gender', 'Number'}, 'V': {'Finiteness'}}
        
    def __init__(self, word, lemma, category, features={}):
        self.word = word
        self.lemma = lemma
        self.category = category
        self.features = features
        #assert self.has_required_tags()
        
    def has_required_tags(self):
        if self.category not in POSTaggedWord.catset:
            return False
        if self.category not in POSTaggedWord.require_tag:
            return not self.features
        common_tags = set()
        for tag_class in POSTaggedWord.require_tag[self.category]:
            common_tags.update(POSTaggedWord.tagset[tag_class].intersection(self.features))
        if common_tags != self.features:
            for tag in common_tags:
                if tag in POSTaggedWord.require_tag:
                    for tag_class in POSTaggedWord.require_tag[tag]:
                        common_tags.update(POSTaggedWord.tagset[tag_class].intersection(self.features))
        return common_tags == self.features
    
    def __str__(self):
        return self.word + ' [' + self.lemma + '] ' + self.category + ' ' + ' '.join(self.features)

def main():
    w = POSTaggedWord("Comendo", "comer", "V", {'GER'})
    y = POSTaggedWord("Como", "como", "KS")
    print(w, w.has_required_tags())
    print(y, y.has_required_tags())

if __name__ == '__main__':
    main()
