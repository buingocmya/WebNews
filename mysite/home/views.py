from django.shortcuts import render
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import requests
import math
from googletrans import Translator


def wup_simi(text1, text2):
    if (text1 == text2):
        return 1.0;
    w1 = wn.synsets(text1)
    w2 = wn.synsets(text2)
    maxScore = 0
    for synset1 in w1:
        for synset2 in w2:
            currScore = wn.wup_similarity(synset1, synset2)
            if currScore > maxScore:
                maxScore = currScore
    #print(text1 + ' ' + text2+ ' ', maxScore)
    return maxScore


def test(request):
    #next = request.GET('next','')
    eng =  request.POST.get('engsenten')
    viet =  request.POST.get('vietsenten')
    submit = request.POST.get('submit')

    viet=trans(viet)
    print (viet)

    englist = preprocessing(eng)
    vietlist= preprocessing(viet)
    
    #result = 0.5 * simiS(englist,vietlist) + 0.5 * simiR(englist,vietlist) 
    result = round(result *100,2)
    context= {'engsenten': preprocessing(eng), 'vietsenten': preprocessing(viet), 'submit': submit, 'result': result}
    print ("result: ",result)
    return render(request, 'news.html', context )

def get_home(request):
    return render(request,'news.html')

def testfunction(request):
    result = "Hello"
    context= {'result': result}
    return render(request,'news.html', context)

def trans(text):
    translate = Translator()
    result = translate.translate(text)
    return result.text

def preprocessing(text):
    #bỏ in hoa
    text = text.lower()
    #bỏ dấu câu
    text = text.translate(str.maketrans('', '', string.punctuation))
    #bỏ stopword
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    
    #bỏ đuôi V
    #wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}
    lemmatizer = WordNetLemmatizer()
    lem_sentence=[]
    for word in filtered_sentence: # or filtered_sentence:
        lem_sentence.append(lemmatizer.lemmatize(word))
        #lem_sentence.append(" ")
    
    
    #trả về từ gốc (eng)
    stem_sentence=[]
    for word in lem_sentence:
        stem_sentence.append(PorterStemmer().stem(word))
        #stem_sentence.append(" ")
    
    return stem_sentence;
    #return "".join(stem_sentence)
    #return "".join(lem_sentence)

"""
#0. run XAMPP
#1. cd mysite
#2. python manage.py migrate
#3. python manage.py runserver 8888
"""

