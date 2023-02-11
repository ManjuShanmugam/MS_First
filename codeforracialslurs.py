import pandas as pd
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


exceldata = pd.read_excel('input.xlsx')

# Having an excel containing the link of the articles/tweets

stopwordstemp = nltk.corpus.stopwords.words('english')
fh1 = open('AllStopWords.txt', 'r')
# all the negative words are are called stop words which help in calculating the prof score
Lines = fh1.readlines()

for index, row in exceldata.iterrows():
    page = requests.get(row["URL"],headers={"User-Agent": "XY"})
    soup = BeautifulSoup(page.content, 'html.parser')
    id =row["URL_ID"]
    with open(f"{id}.txt", "w") as f:
        page_title=soup.title.text
        f.writelines(page_title)
        for data in soup.find_all("p"):
            sum = data.get_text()
            f.writelines(sum)
        f.close()
    with open(f"{id}.txt", "r") as fh2:
        fh2lines=fh2.read()
        fh2tokens = word_tokenize(fh2lines)
#print(fh2tokens)
    tokens_without_sw = [word for word in fh2tokens if not word in Lines]
#print(tokens_without_sw)
    print('\n\n')
    # Having extracted the data/tweets from web, tokenised the data to find if it matches the negative wordslist, if the match happens then the negative score is incremented by 1
    fh3 = open('negativewords.txt', 'r')
    fh3lines=fh3.read()
    fh3tokens = word_tokenize(fh3lines)
    tokens_negative=[word for word in tokens_without_sw if word in fh3tokens]
    #print(tokens_negative)
    ns=0
    for word in tokens_negative:
        ns=ns-1
    ns=ns*(-1)
    print(ns)
    fh4 = open('prof_score.txt', 'w')
    fh4.write(ns)
    
    
    
fh2.close()
fh3.close()
fh4.close()

    