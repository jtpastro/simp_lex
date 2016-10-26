#!/usr/bin/env python3

import requests,sys
from html.parser import HTMLParser
from collections import defaultdict

class Inflector:
    def analyze(self):
        pass

#session = requests.Session()
class LXInflector(Inflector):
    def __init__(self, features):
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        if features[1] == 'v':
            url = 'http://lxcenter.di.fc.ul.pt/services/online_conj/cgi-bin/flex.cgi'
            data = {'lemma' : features[0],
                     'type' : 'none',
                     'lang' : 'pt'
                     }
            cookies = {'PHPSESSID':'5s5ae6gohhc3ehq5an6r1ph4a7'}
            p = requests.get(url, cookies=cookies, headers=headers, params=data)
            parser = VerbalParser()
            parser.feed(p.text)
            self.res = parser.response[LXInflector.tags(features[2], features[3], features[4])]
        elif features[1] == 'cn' or features[1] == 'adj':
            cookies = {'JSESSIONID':'B78A2BD39CC55193A078A637B295F6ED', }
            url = 'http://nlxserv.di.fc.ul.pt/lxinflector/pt/Flex_pt.jsp'
            data = {    "categoria" : features[1], #"cn", #adj
                        "palavra" : features[0],
                        "submit" : "Flexionar",
                        "genero" : features[2],#"m", #f
                        "numero" : features[3] #"s" #p
                    }
            p = requests.post(url, cookies=cookies, headers=headers, data=data)
            parser = NominalParser()
            parser.feed(p.text)
            self.res = parser.response

    def tags(mood, tense, person):
        tags = {"1S":1, "1P":4, "2S":2, "2P":5, "3S":3, "3P":6, "1/3S":3, "0/1/3S":3,
                "PR":1, "IMPF":3, "PS":5, "MQP":6, "FUT":8, "COND":10, "IND":1, "SUBJ":2, "IMP":3,
                "INF":4, "PCP":6, "GER":5}
        return (tags[mood] if mood in tags else 0, 
                tags[tense] if tense in tags else 0,
                tags[person] if person in tags else 0)
    
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
    modes = defaultdict(int, {
	 'conjuntivo' : 2 ,
	 'particípio passado' : 6 ,
	 'gerúndio' : 5 ,
	 'infinitivo' : 4 ,
	 'imperativo' : 3 ,
	 'indicativo' : 1 
    })
    tenses = defaultdict(int, {
	 'pretérito' : 5 ,
	 'infinitivo pessoal presente' : 14 ,
	 'pretérito perfeito composto' : 2 ,
	 'afirmativo' : 12 ,
	 'presente' : 1 ,
	 'futuro do pretérito composto' : 11 ,
	 'pretérito imperfeito' : 3 ,
	 'futuro composto' : 11 ,
	 'futuro do presente composto' : 9 ,
	 'pretérito perfeito simples' : 5 ,
	 'pretérito mais-que-perfeito simples' : 6 ,
	 'infinitivo pessoal pretérito' : 15 ,
	 'infinitivo impessoal pretérito' : 17 ,
	 'futuro simples' : 8,
	 'futuro do presente simples' : 8 ,
	 'infinitivo impessoal presente' : 16 ,
	 'pretérito mais-que-perfeito anterior' : 7 ,
	 'negativo' : 13 ,
	 'pretérito mais-que-perfeito' : 6 ,
	 'pretérito perfeito' : 5 ,
	 'pretérito mais-que-perfeito composto' : 4 ,
	 'futuro do pretérito simples' : 10 ,
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
                    self.response[(VerbalParser.modes[self.mode.lower()], VerbalParser.tenses[self.tense[i].lower()], VerbalParser.person[(self.pronoun+[None])[0]])] = self.verb[i]
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
