from re import sub
from nltk.probability import FreqDist
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from heapq import nlargest


res = requests.get(input("enter a link to summarise"))
s = BeautifulSoup(res.content,"html.parser")
paragraphs = s.find_all("p")
p=""
for i in paragraphs:
    p+=i.text



p = sub(r'\\s+',' ',p) #removes extra spaces

words_list = [i for i in word_tokenize(p) if i not in stopwords.words('English') and i.isalpha()]
words = ""
for i in words_list:
    words+="{} ".format(i)

token = sent_tokenize(p)

freqs = FreqDist(word_tokenize(words))


max_freq = max(freqs.values())

#converting to relative frequencies
for f in freqs.keys():
    freqs[f] = (freqs[f]/max_freq)

sent_scores = {}
for sent in token:
    for word in word_tokenize(sent.lower()):
        if word in freqs.keys():
            if len(sent.split(" "))<30:
                if sent not in sent_scores.keys():
                    sent_scores[sent]=freqs[word]
                else:
                    sent_scores[sent]+=freqs[word]

summary_sentences = nlargest(10,sent_scores,key=sent_scores.get)
summary=""
for sent in summary_sentences:
    summary+="{} ".format(sent)


print(summary)