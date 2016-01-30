from os import system
from googlefinance import getQuotes
from random import randint
import json
import speech_recognition as sr
import re
import subprocess
#global variables
dataFile='test.txt'
settingsFile='jaxSettings.json'
connected = False
loud=False



#Utilities 
def testConnection():
	data=subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport","-I"])
	try:
		strength=abs(int(data[int(data.find("agrCtlRSSI:"))+11:int(data.find("agrCtlRSSI:"))+15]))
		if strength>70:
			return False
		else:
			return True
	except ValueError as err:
		return False
		pass

def getStockData(stock):
	#Returns stock price 
	try:
		data=getQuotes(stock)
		for i in data:
			sentence=i['StockSymbol']+" was traded at "+i['LastTradePrice']+" at "+i["LastTradeTime"]
		return sentence
	except:
		say("Error, could not find stock "+ stock)
	
	#print json.dumps(data)
	

def changeDefaultSettings(key=None,value=None):
#Change the default settings for JAX	
	global loud
	global connected
	if key==None:
		cmd=getAnswer("Enter the variable you wish to change, or ls for possibilities: ").lower()
	else:
		cmd=key
	if cmd == "ls":
		print "\nloud: ("+str(loud)+") True, False\nconnected: ("+str(connected)+") True, False \n"
		changeDefaultSettings()
	elif any(x in cmd for x in ["loud","connected"]):
			if value==None:
				value=getAnswer("What would you like to change it to?")
				value=value.lower()
			replaceJson(settingsFile,cmd,value)
	else:
		print("Variable not recognized")

	setSettings()


	# elif cmd=="loud":
	# 	loud=raw_input("What would you like to change it to?\n:")
	# 	loud="True" in loud
	# 	replaceJson(settingsFile,cmd,loud)
	# elif cmd=="connected":
	# 	answer=raw_input("What would you like to change it to?\n:")
	# 	if any(x in answer for x in ["true","yes"]) and testConnection()==True:
	# 		connected=True
	# 		replaceJson(settingsFile,cmd,connected)
	# 	elif any(x in answer for x in ["true","yes"]) and testConnection()==False:
	# 		print("Sorry, your internet is not fast enough.\n")
	# 		connected=False
	# 		replaceJson(settingsFile,cmd,connected)
	# 	else:
	# 		connected=False
	# 		replaceJson(settingsFile,cmd,connected)



def replaceJson(file,key,value):
	with open(file) as data_file:
		data = json.load(data_file)
	data[key]=value
	with open(file,'w') as outfile:
		json.dump(data, outfile)

def setSettings():
	global loud
	global connected
	loud= "true"==readJson(settingsFile,"loud").lower() 
	connected="true" == readJson(settingsFile,"connected").lower() and testConnection()
#==========================


#Communication

def getAnswer(question,loud=None,connection=None):
#Asks question and returns speech to text

	if connected == True:
		say(question)
		r = sr.Recognizer()
		with sr.Microphone() as source:
			audio = r.listen(source)
		# print r.recognize_google(audio).lower()
		return r.recognize_google(audio).lower()
	else:
		say(question)
		return raw_input(": ").lower()

def say(text):
    print text
    if loud==True:
    	system('say '+text)
    



#==========================


# File interaction methods=============

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

def readJson(file,key):
	with open(file) as data_file:
		data = json.load(data_file)
	return data[key]


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
	sentence=getAnswer("Give me a command",)
	if inFile(sentence):
		print sentence + " in file"
	else:
		write(sentence)

#====================================

#Startup processes 
# def init():
# 	command=getAnswer("Hello User, my name is jacks. How can I help you today?")





def setup():
	global connected
	global loud
	if testConnection() == True:
		say("Your internet is fast enough for JAX voice communication.")
		answer=getAnswer("Do you want to speak to JAX?")
		if any(x in answer for x in ["yes","y","yep"] ):
			connected=True
	else:
		connected=False
		say("Your internet is not fast enough for JAX voice communication, you will have to talk to him through text.")

	answer=getAnswer("Do you want JAX to speak?")
	if any(x in answer for x in ["yes","y","yep"] ):
		loud=True
		say("Then I will speak")
	else:
		say("Then I won't speak!")

def executeCommand(command):
	if "stock" in command:
		stock=getAnswer("What stock would you like to research?").encode('ascii','ignore')
		say(getStockData(stock))
	if "setting" in command:
		changeDefaultSettings()
	if "ls" in command:
		print "loud: ("+str(loud)+") True, False\nconnected: ("+str(connected)+") True, False \n"

#==========================

def startup():
	setSettings()
	userInput=""
	while userInput!="quit":
		userInput=getAnswer("What can I do for you, quit for exit.")
		executeCommand(userInput)


def init():
	com=getAnswer("What can I do for you today")
	say("I heard "+com)
	if "stock" in com or "stocks" in com:
		stock=getAnswer("What stock would you like to research?").encode('ascii','ignore')
		say(getStockData(stock))





#Startup processes 
startup()
