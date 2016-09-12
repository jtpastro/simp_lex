#!/usr/bin/env python3

import requests,sys
from html.parser import HTMLParser

#session = requests.Session()
class POSTagger:
    def __init__(self,argv):
        cookies = {'VISLSessionID':'434001961b9d41df08406bb455784ff2', 'VISLLastLanguage':'pt', 'VISLUniqueID':'e698acd58e6bd5fd383f0a2096a399495c185618'}
        url = 'http://visl.sdu.dk/visl/pt/parsing/automatic/parse.php'
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        data = {'text':' '.join(argv), 'parser':'morphdis', 'visual':'niceline'}
        p = requests.post(url, cookies=cookies, headers=headers, data=data)

        self.parser = PalavraParser()
        self.parser.feed(p.text)
    
    def analyze(self):
        return self.parser.response[1:-1]

class PalavraParser(HTMLParser):
    def __init__(self):
        super(PalavraParser, self).__init__()
        self.startResponse = False
        self.response=[""]
    def handle_starttag(self, tag, attrs):
        if self.startResponse == False:
            if tag == 'dl':
                self.startResponse=True
        elif tag == 'dt':
            self.response[-1] = self.response[-1].split()
            self.response.append("")
    def handle_endtag(self, tag):
        if self.startResponse == True and tag == 'dl':
            self.startResponse = False
    def handle_data(self, data):
        if self.startResponse and data and self.response:
            self.response[-1] += data

def main(argv):
    print(POSTagger(argv).analyze())

if __name__ == "__main__":
    main(sys.argv[1:])
