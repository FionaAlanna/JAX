# from os import system
import os
from googlefinance import getQuotes
from random import randint
import json
import speech_recognition as sr
import re
import subprocess
#global variables
dataFile='jaxData.txt'
settingsFile='jaxSettings.json'
commandFile="jaxCommands.json"
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
		template = "{0:20}{1:20}{2:20}"
		print template.format("Variable","Current","Options")
		print template.format("loud:",str(loud),"True, False")
		print template.format("connected:",str(connected),"True, False")+"\n"
		changeDefaultSettings()
	elif any(x in cmd for x in ["loud","connected"]):
			if value==None:
				value=getAnswer("What would you like to change it to?")
				value=value.lower()
			replaceJson(settingsFile,cmd,value)
	else:
		print("Variable not recognized")

	setSettings()


def setSettings():
	global loud
	global connected
	loud= "true"==readJson(settingsFile,"loud").lower() 
	connected="true" == readJson(settingsFile,"connected").lower() and testConnection()
#==========================


#Communication

def getAnswer(question,connection=None,louder=None):
#Asks question and returns speech to text
	global loud
	global connected
	if connection!=None:
		connected=connection
	if loud!=None:
		loud=louder


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





def readJson(datFile,key):
	try:
		with open(datFile) as data_file:
			data = json.load(data_file)
		return data[key]
	except:
	 	return False

def appendJson(datFile,key,value):
	with open(datFile) as data_file:
		data = json.load(data_file)
		if not data.has_key(key):
			data[key] = value
	with open(datFile,'w') as outfile:
		json.dump(data, outfile)

def deleteJson(datFile,key):
	data  = json.load(open(datFile))                                                 
	for i in data:
		del i[key]
		break

def replaceJson(datFile,key,value):
	with open(datFile) as data_file:
		data = json.load(data_file)
	data[key]=value
	with open(datFile,'w') as outfile:
		json.dump(data, outfile)
	outfile.close()

def jsonifyCommand(com):
	command=readJson(commandFile,com)
	if command==False:
		value=raw_input("This command has not been used before, please enter in the command\n")
		appendJson(commandFile,com,value)
		executeCommand(value)
	else:
		executeCommand(command)

def editCommands(string=None,command=None):
	if string!=None and command!=None:
		replaceJson(commandFile,string,command)
	elif string!=None and command==None:
		replaceJson(commandFile,string,raw_input("Replace current command with:\n"))
	else:
		with open(commandFile) as data_file:
			data=json.load(data_file)
		template = "{0:20}{1:20}"
		print template.format("String","Command")
		for x in data:
			print template.format(x,data[x])
			

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
	words=text.split(" ")
	for i in range(0,len(words)-1):
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

def grabFile(destFile):
	name=subprocess.check_output("whoami").rstrip()
	paths = [line[2:] for line in subprocess.check_output("find . -iname '"+destFile+"'", shell=True,cwd="/Users/"+name).splitlines()]
	if paths==[]:
		print "No file found"
	elif len(paths)==1:
		subprocess.call(["open",paths[0]],cwd="/Users/"+name)
	else:
		i=1
		for string in paths:
			print str(i) +":  "+ string + "\n"  
			i=i+1
		# print "which path?\n"+'\n'.join(paths)
		number=int(getAnswer("Which path?"))
		if number<len(paths) and number>0:
			subprocess.call(["open",paths[number-1]],cwd="/Users/"+name)
		else:
			say("Index out of range")
		

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
	if any(x in answer for x in ["yes","y","yea"] ):
		loud=True
		say("Then I will speak")
	else:
		say("Then I won't speak!")

def executeCommand(command):
	command=command.split()
	if "stock" in command:
		stock=getAnswer("What stock would you like to research?").encode('ascii','ignore')
		say(getStockData(stock))
	if "settings" in command:
		changeDefaultSettings()
	if "ls" in command:
		
		template = "{0:20}{1:20}{2:20}"
		print template.format("Variable","Current","Options")
		print template.format("loud:",str(loud),"True, False")
		print template.format("connected:",str(connected),"True, False")+"\n"
	if "open" in command:
		if len(command)==2:
			grabFile(command[1])
		else:
			grabFile(getAnswer("What file would you like to open?"))
		#build reload command 


#==========================

def startup():
	setSettings()
	userInput=""
	while userInput!="quit()":
		userInput=getAnswer("What can I do for you, quit() for exit.")
		jsonifyCommand(userInput)


#Startup processes 

startup()
