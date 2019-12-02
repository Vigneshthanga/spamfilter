import sys
import glob
import errno
import csv
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
import math

_dict={}
_dict["free"]=1
_dict["click here"]=2
_dict["visit"]=3
_dict["open attachment"]=4
_dict["call this number"]=5
_dict["money"]=6
_dict["out"]=7
_dict["extra"]=8
_dict["offer"]=9
_dict["available"]=10
_dict["pension"]=11
_dict["opportunity"]=12
_dict["chance"]=13
_dict["investment"]=14

doc_len = 6 # total number of documents

def preprocess(text):
    words_list = ""
    sstemmer = SnowballStemmer("english")
    lemmatizer = WordNetLemmatizer()
    text = text.split()
    for w in text:
        w = lemmatizer.lemmatize(w)
        words_list = words_list + sstemmer.stem(w) + " "
    return words_list

path = './*.txt'
files = glob.glob(path)
ls = []
for name in files:
    try:
        with open(name) as f:
            ls.append(f.readlines())
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

_mat= []
for row in ls:
    for text in row:
        _ls = preprocess(text).split()
        _arr =[]
        for i in range(len(_dict)):
            _arr.append(0)
        print(_ls)
        for word in _ls:
            if (word in _dict):
                print(word)
                _arr[_dict[word]-1] += 1
        _mat.append(_arr)

print(_dict.keys())
for row in _mat:
    print(row)

def find_term(idx):
    count = 0
    for i in range(len(_mat)):
        row = _mat[i]
        if (row[idx] != 0):
            count+=1
    return count

print(list(_dict.keys())[list(_dict.values()).index(12)])

j=0
for row in _mat:
    i=0
    df = 0
    for val in row:
        if (val != 0):
            if (val == 1):
                tf = 1
            else:
                tf = 1 + math.log((1+math.log(val,10)),10)
            df = find_term(i)
            idf = 0
            if df != 0:
                idf = math.log(((1+doc_len)/df),10)
            print("TF.IDF of D"+str(j)+" and "+str(list(_dict.keys())[list(_dict.values()).index(i+1)])+" "+str(tf*idf))
        i+=1
    j+=1
