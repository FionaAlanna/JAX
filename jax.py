from os import system
from googlefinance import getQuotes
from random import randint
import json
import speech_recognition as sr
import subprocess
#global variables
dataFile="test.txt"

def say(text):
        system('say '+text)

def getStockData(stock):
    #Returns stock price 
    data=getQuotes(stock)
        for i in data:
                sentence=i['StockSymbol']+" was traded at "+i['LastTradePrice']
    print json.dumps(data)
    return sentence

def listen(question):
    #Asks question and returns speech to text
        say(question)
    r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        print(r.recognize_google(audio))
    return r.recognize_google(audio).lower()

#File interaction methods=============

def inFile(text):
    #returns if a string is in a file
    f=open(dataFile,'r')
    if text.lower() in f.read():
        return True
        f.close()
    else:
        return False
        f.close()

def writeCommand(text):
    #Writes text to the file
    if not inFile(text):
        f=open(dataFile,'a')
        f.write(text.lower()+":\n")
        f.close()

def replace(original,replacement):
    f=open(dataFile,'r')
    data=f.read()
    f.close()
    print "old: " + data
    data=data.replace(original,replacement)
    print "new: " + data
    f=open(dataFile,'w')
    f.writeCommand(data)
    f.close()

#=====================================

#Responses============================
def getRandomResponse():
    f=open('jaxResponses.txt','r')
    data=f.readlines()
    f.close()
    com=data[randint(1,len(data)-1)]
    return com[com.find("|;|")+3:].rstrip('\n')
def getConnotationResponse(number):
    f=open('jaxResponses.txt','r')
    data=f.readlines()
    f.close()
    contained=False
    choices=[]
    for com in data:
        if "|:|"+str(number)+"|;|" in com:
            choices.append(com[com.find("|;|")+3:].rstrip('\n'))
            contained=True
    if contained:
        return choices
    else:
        return False

#=====================================



def decode(text):
    text=text.lower()
    words=text.split(" ")
    for i in range(0,len(words)):
        print type(i)
        if words[i]=="open":
            #subprocess.call(["cd","Desktop"])
            subprocess.call(["open",words[i+1]])
        if words[i]=="switch":
            print "switch"
            #subprocess.call(["cd","Applications"])
            #subprocess.call(["open","http://www.apple.com/","-a","Google Chrome"])

def test():
    sentence=listen("Give me a command")
    if inFile(sentence):
        print sentence + " in file"
    else:
        write(sentence)

# def graph():
#    graph = {'A': ['B', 'C'],
#              'B': ['C', 'D'],
#              'C': ['D'],
#              'D': ['C'],
#              'E': ['F'],
#              'F': ['C']}






def init():
    com=listen("speak please")
    print type(com)
    print "I heard "+com
    if "stock" in com or "stocks" in com:
        stock=listen("What stock would you like to research?").encode('ascii','ignore')
        say(getStockData(stock))
