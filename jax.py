from os import system
from googlefinance import getQuotes
import json
import speech_recognition as sr
def say(text):
        system('say '+text)
def getSummary(stock):
        data=getQuotes(stock)
        for i in data:
                sentence=i['StockSymbol']+" was traded at "+i['LastTradePrice']
        say(sentence)
def listen():
	say("I am listening")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        print(r.recognize_google(audio))






say('Hello, I am JACKS. What can I help you with?')

                                          
