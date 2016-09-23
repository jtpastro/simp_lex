#!/usr/bin/env python3

import requests,sys
from html.parser import HTMLParser
from collections import defaultdict

class Inflector:
    def analyze(self):
        pass

#session = requests.Session()
class LXInflector(Inflector):
    def __init__(self,argv):
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        if argv[1] == 'v':
            url = 'http://lxcenter.di.fc.ul.pt/services/online_conj/cgi-bin/flex.cgi'
            data = {'lemma' : argv[0],
                     'type' : 'none',
                     'lang' : 'pt'
                     }
            cookies = {'PHPSESSID':'5s5ae6gohhc3ehq5an6r1ph4a7'}
            p = requests.get(url, cookies=cookies, headers=headers, params=data)
            parser = VerbalParser()
            parser.feed(p.text)
            self.res = parser.response
        elif argv[1] == 'cn' or argv[1] == 'adj':
            cookies = {'JSESSIONID':'B78A2BD39CC55193A078A637B295F6ED', }
            url = 'http://nlxserv.di.fc.ul.pt/lxinflector/pt/Flex_pt.jsp'
            data = {    "categoria" : argv[1], #"cn", #adj
                        "palavra" : argv[0],
                        "submit" : "Flexionar",
                        "genero" : argv[2],#"m", #f
                        "numero" : argv[3] #"s" #p
                    }
            p = requests.post(url, cookies=cookies, headers=headers, data=data)
            parser = NominalParser()
            parser.feed(p.text)
            self.res = parser.response
    
    def analyze(self):
        return self.res

class NominalParser(HTMLParser):
    def __init__(self):
        super(NominalParser, self).__init__()
        self.startResponse = False
        self.response = ''
        self.lastTag = ''
    def handle_starttag(self, tag, attrs):
        self.lastTag = tag
    def handle_endtag(self, tag):
        if tag == 'table':
            self.startResponse = False
    def handle_data(self, data):
        if 'Palavra pedida:' in data:
            self.startResponse = True
        elif self.startResponse and self.lastTag == 'b':
            data = data.split()[0]
            if data:
                self.response = data

class VerbalParser(HTMLParser):
    modes = defaultdict(int,
            {   'Indicativo':1,
                'Conjuntivo':2,
                'Imperativo':3,
                'Infinitivo':4,
                'Gerúndio' : 5,
                'Particípio Passado' : 6
            })
    tenses = defaultdict(int, 
        {   'Presente' : 1,
            'Pretérito Perfeito Composto' : 2,
            'Pretérito Imperfeito' : 3,
            'Pretérito Mais-Que-Perfeito Composto': 4,
            'Pretérito Perfeito Simples' : 5,
            'Pretérito Mais-Que-Perfeito Simples': 6,
            'Pretérito Mais-Que-Perfeito Anterior': 7,
            'Futuro do Presente Simples' : 8,
            'Futuro do Presente Composto' : 9,
            'Futuro do Pretérito Simples' : 10,
            'Futuro do Pretérito Composto' : 11,
            'Pretérito Perfeito' : 5,
            'Pretérito Mais-Que-Perfeito': 6,
            'Futuro Simples' : 10,
            'Futuro Composto' : 11,
            'Afirmativo' : 12,
            'Negativo' : 13,
            'Infinitivo Pessoal Presente' : 14,
            'Infinitivo Pessoal Pretérito' : 15,
            'Infinitivo Impessoal Presente' : 16,
            'Infinitivo Impessoal Pretérito' : 17,
            'Presente' : 1,
            'Pretérito' : 6
        })
    person = defaultdict(int,
        {   'eu' : 1,
            'tu' : 2,
            'ele' : 3,
            'ela' : 3,
            'você' : 3,
            'nós' : 4,
            'vós' : 5,
            'eles': 6,
            'elas': 6,
            'vocês' : 6
        })
    def __init__(self):
        super(VerbalParser, self).__init__()
        self.startResponse = False
        self.response = {}
        self.pronoun = []
        self.verb = []
        self.tense = []
        self.mode = ''
        self.curClass = ''
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table'and 'class' in  attrs and attrs['class'] == 'conjugation':
            self.startResponse = True
        elif self.startResponse == True:
            if tag == 'th' and 'class' in attrs:
                self.curClass = attrs['class']
            elif tag == 'span' and 'class' in attrs:
                if attrs['class'] == 'extra':
                    self.curClass = 'pronome'
            elif tag == 'a' and self.curClass != 'composto':
                self.curClass = 'verbo'
    def handle_endtag(self, tag):
        if tag == 'table':
            self.startResponse = False
        elif tag == 'tr' and self.curClass in ('verbo', 'composto', 'pronome'):
            for i in range(len(self.tense)):
                self.response[(VerbalParser.modes[self.mode], VerbalParser.tenses[self.tense[i]], VerbalParser.person[(self.pronoun+[None])[0]])] = self.verb[i]
            self.pronoun = []
            self.curClass = ''
            self.verb = []
    def handle_data(self, data):
        if data == u'\u00A0':
            self.tense = []
        elif data.strip():
            if self.curClass == 'modo':
                self.tense = []
                self.mode = data
            elif self.curClass == 'tempo':
                self.tense.append(data)
            elif self.curClass == 'pronome':
                if data == '/':
                    self.curClass = 'composto'
                elif not self.pronoun:
                    self.pronoun = data.split('/ ')
            elif self.curClass == 'verbo':
                self.verb.append([data])
            elif self.curClass == 'composto':
                self.verb[-1] = [self.verb[-1][0] + ' ' + data.split()[1]]
                self.verb[-1].append(data)

def main(argv):
    print(LXInflector(argv).analyze())

if __name__ == "__main__":
    main(sys.argv[1:])