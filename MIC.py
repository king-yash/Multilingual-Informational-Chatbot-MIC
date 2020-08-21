#import libraries
from newspaper import Article
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings
from googletrans import Translator
#ignore warnings
warnings.filterwarnings('ignore')
#download the packages from NLTK
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
#asking user for URL
print("MIC : Hi, I am MIC, your personal multilinguial chatbot, please enter the URL of your choice from which you want to retrieve information")
URL = input("You : ")
#article URL
article = Article(URL)#user will enter URL of his/her choice
article.download()
article.parse()
article.nlp()
corpus = article.text
#initializing translater
translator = Translator()
#tokenization
text = corpus
sent_tokens = nltk.sent_tokenize(text)
#creating a dictionary (key:value) pair to remove punctuation
remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)
#creating a function to return a list of lemmatized lower case words
def LemNormalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))
#keyword matching
GREETINGS_INPUTS = ["hi", "hello", "greetings", "wassup", "hey"]
GREETINGS_RESPONSES = ["howdy", "hi", "hey", "what's good", "hello", "hey there"]
#creaitng a function to return a random greeting
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETINGS_INPUTS:
            return random.choice(GREETINGS_RESPONSES)
#generating function for response
def response(ur):
    #user response query
    ur = ur.lower()
    #chatbot response
    rr = ""
    #append user response to sentence list
    sent_tokens.append(ur)
    #create a TfidffVectorizer object
    TfidfVec = TfidfVectorizer(tokenizer = LemNormalize, stop_words='english')
    #convert text to matrix of TF-IDF features
    tfidf = TfidfVec.fit_transform(sent_tokens)
    #similarity score
    vals = cosine_similarity(tfidf[-1], tfidf)
    #get index of most similar sentence to the user response
    idx = vals.argsort()[0][-2]
    #reduce dimensiolity of vals
    flat = vals.flatten()
    #sort List
    flat.sort()
    #most similar score
    score = flat[-2]
    #if the var score is 0 then their is no text similar to User
    if score == 0:
        rr = rr+"Sorry, I was not able to retrieve any information"
    else:
        rr = rr+sent_tokens[idx]
    sent_tokens.remove(ur)
    return rr
#asking user for prefered language
print("MIC : Please enter your prefered language.\nThe available options are:-\n1. English - en\n2. French - fs\n3. Italian - it\n4. Portugese - pt\n5. Spanish - es")
x = input("You : ")
while True:
    if x == "en" or x == "fr" or x == "it" or x == "pt" or x == "es":
        pref_lang = x
        break
    else:
        print("MIC : Entered option is not available.")
        print("MIC : Please enter your prefered language again.")
        x = input("You : ")
        continue
#application working
print("MIC : " + translator.translate("Hello!",dest=pref_lang).text)
print("MIC : " + translator.translate("To change the prefered language, type - ",dest=pref_lang).text + " change.")
print("MIC : " + translator.translate("To exit, type - ",dest=pref_lang).text + " bye.")
while True:
    sen=input("You : ")
    sen=translator.translate(sen,dest='en').text
    if sen == "change":
        print("MIC : " + translator.translate("Please enter new prefered language.",dest=pref_lang).text)
        x = input("You : ")
        while True:
            if x == "en" or x == "fr" or x == "it" or x == "pt" or x == "es":
                pref_lang = x
                break
            else:
                print("MIC : " + translator.translate("Entered option is not available.",dest=pref_lang).text)
                print("MIC : " + translator.translate("Please enter your prefered language again.",dest=pref_lang).text)
                x = input("You : ")
                continue
    elif sen == "bye":
        print("MIC : " + translator.translate("See you next time,bye",dest=pref_lang).text)
        break
    elif sen == "thanks" or sen == "thank you":
        print("MIC : " + translator.translate("You are welcome",dest=pref_lang).text)
    elif greeting(sen)!=None:
        print("MIC : " + translator.translate(greeting(sen),dest=pref_lang).text)
    else:
        r=response(sen)
        print("MIC : " + translator.translate(r,dest=pref_lang).text)
