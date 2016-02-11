from os import system
import os
from googlefinance import getQuotes
from random import randint
import json
import speech_recognition as sr
import re
import subprocess
import shelve
from gtts import gTTS
#global variables
user = "conor"
dataFile=user+'JaxData.txt'
settingsFile=user+'JaxSettings.json'
commandFile=user+"JaxCommands.json"
studyFile=user+"JaxStudy.json"
connected = False
loud = False
r = sr.Recognizer()
m = sr.Microphone()
info={}

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

def setLocalSettings(variable,value):
	if variable=="loud":
		global loud
		loud="true" in value.lower()
	elif variable=="connected":
		global connected
		connected="true" in value.lower()
	elif variable == "user":
		global user
		user= value.lower()

def getDefaultSettings():
	global loud
	global connected
	loud= "true"==readJson(settingsFile,"loud").lower() 
	connected="true" == readJson(settingsFile,"connected").lower() and testConnection()
	user=readJson(settingsFile,"user")
#==========================


#Communication

def getAnswer(question,connection=None,louder=None):
#Asks question and returns speech to text
	# global loud
	# global connected
	# if connection!=None:
	# 	connected=connection
	# if loud!=None:
	# 	loud=louder
	if connected == True:
		say(question)
		r = sr.Recognizer()
		with sr.Microphone() as source:
			audio = r.listen(source,timeout=100)
		# print r.recognize_google(audio).lower()
		try:
			return r.recognize_google(audio).lower()
		except sr.UnknownValueError:
			getAnswer("Did not understand, please repeat")
		except sr.RequestError:
			say("Could not connect, please switch off connected")

	else:
		say(question)
		return raw_input(": ").lower()





def say(output):
    print output
    tts= gTTS(text=output,lang='en')
    tts.save("speech.mp3")
    subprocess.call(["afplay","speech.mp3"])
    # if loud==True:
    # 	system('say '+text)
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

def readJson(datFile,key,upperKey=None):
	try:
		with open(datFile) as data_file:
			data = json.load(data_file)
		if upperKey==None:
			return data[key]
		else:
			return data[upperKey][key]
	except:
	 	return False

def appendJson(datFile,key,value,upperKey=None):
	with open(datFile) as data_file:
		data = json.load(data_file)
		if upperKey==None:
			if not data.has_key(key):
				data[key] = value
		else:
			if not data[upperKey].has_key(key):
				data[upperKey][key]=value
	with open(datFile,'w') as outfile:
		json.dump(data, outfile,sort_keys=True)

def deleteJson(datFile,key,upperKey=None):
	with open(datFile) as data_file:
		data  = json.load(data_file)                                                
	try:
		if upperKey==None:
			del data[key]
		else:
			del data[upperKey][key]
		with open(datFile,'w') as outfile:
			json.dump(data,outfile)
	except:
		return False

def replaceJson(datFile,key,value,upperKey=None):
	with open(datFile) as data_file:
		data = json.load(data_file)
	if upperKey==None:
		data[key]=value
	else:
		data[upperKey][key]=value
	with open(datFile,'w') as outfile:
		json.dump(data, outfile)

def jsonifyCommand(com):
	#exlusions:
	splitc=com.split()
	if "google" in com and "open" not in com:
		executeCommand(com)
		return
	if any(x in splitc for x in ["craigslist","buy","c"]):
		if len(splitc)==3:
			# buy datsun fresno
			executeCommand("openb "+"https://"+splitc[2]+".craigslist.org/search/sss?sort=rel&query="+splitc[1])
			return
	if "read" == splitc[0]:
		executeCommand(com)
		return
	command=readJson(commandFile,com)
	if command==False:
		value=raw_input("This command has not been used before, please enter in the command\n:")
		if any(x in value for x in ["copy","cp"]):
			value=value.replace("copy ","")
			value=readJson(commandFile,value)
			appendJson(commandFile,com,value)
		else:
			appendJson(commandFile,com,value)
		executeCommand(value)
	else:
		executeCommand(command)



# def shelvify(obj):
# 	d = shelve.open("lingFile") # open, with (g)dbm filename -- no suffix
# 	d["graph"] = obj  # store data at key (overwrites old data if
# 	data = d["graph"]   # retrieve a COPY of the data at key (raise
#     # delete data stored at key (raises KeyError
# 	#flag = "key" in d # true if the key exists
# 	#list = d.keys() # a list of all existing keys (slow!)
# 	print data
# 	d.close()       # close it


# class Vertex:
#     def __init__(self, node):
#         self.id = node
#         self.adjacent = {}

#     def __str__(self):
#         return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

#     def add_neighbor(self, neighbor, weight=0):
#         self.adjacent[neighbor] = weight

#     def get_connections(self):
#         return self.adjacent.keys()  

#     def get_id(self):
#         return self.id

#     def get_weight(self, neighbor):
#         return self.adjacent[neighbor]

# class Graph:
#     def __init__(self):
#         self.vert_dict = {}
#         self.num_vertices = 0

#     def __iter__(self):
#         return iter(self.vert_dict.values())

#     def add_vertex(self, node):
#         self.num_vertices = self.num_vertices + 1
#         new_vertex = Vertex(node)
#         self.vert_dict[node] = new_vertex
#         return new_vertex

#     def get_vertex(self, n):
#         if n in self.vert_dict:
#             return self.vert_dict[n]
#         else:
#             return None

#     def add_edge(self, frm, to, cost = 0):
#         if frm not in self.vert_dict:
#             self.add_vertex(frm)
#         if to not in self.vert_dict:
#             self.add_vertex(to)

#         self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
#         self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

#     def get_vertices(self):
#         return self.vert_dict.keys()


# g = Graph()






# g.add_vertex('a')
# g.add_vertex('b')
# g.add_vertex('c')
# g.add_vertex('d')
# g.add_vertex('e')
# g.add_vertex('f')

# g.add_edge('a', 'b', 7)  
# g.add_edge('a', 'c', 9)
# g.add_edge('a', 'f', 14)
# g.add_edge('b', 'c', 10)
# g.add_edge('b', 'd', 15)
# g.add_edge('c', 'd', 11)
# g.add_edge('c', 'f', 2)
# g.add_edge('d', 'e', 6)
# g.add_edge('e', 'f', 9)

# # for v in g:
# #     for w in v.get_connections():
# #         vid = v.get_id()
# #         wid = w.get_id()
# #         print '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w))

# # for v in g:
# #     print 'g.vert_dict[%s]=%s' %(v.get_id(), g.vert_dict[v.get_id()])

# shelvify(g)




def editCommands(string=None,command=None):
	if string=="none":
		return
	elif string!=None and command!=None:
		if readJson(commandFile,string)!=False:
			replaceJson(commandFile,string,command)
		else:
			editCommands(getAnswer("Command not found, please retype"))

	elif string!=None and command==None:
		if readJson(commandFile,string)==False:
			editCommands(getAnswer("Command not found, please retype"))
		elif getAnswer("Replace or delete?")=="replace":
			replaceJson(commandFile,string,raw_input("Replace current command with\n:"))
		else:
			deleteJson(commandFile,string)
	
	else:
		with open(commandFile) as data_file:
			data=json.load(data_file)
		
		template = "{0:30}{1:30}"
		print template.format("String","Command")
		for x in data:
			print template.format(x,data[x])
		editCommands(getAnswer("Which command would you like to edit? None to cancel."))
			

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

def grabFile(destFile):
	if "." not in destFile:
		destFile=destFile+".*"
	name=subprocess.check_output("whoami").rstrip()
	paths = [line[2:] for line in subprocess.check_output("find . -iname '"+destFile+"'", shell=True,cwd="/Users/"+name).splitlines()]
	if paths==[]:
		print "No file found"
	elif len(paths)==1:
		subprocess.call(["open",paths[0]],cwd="/Users/"+name)
		return "/Users/"+name+"/"+paths[0]
	else:
		i=1
		for string in paths:
			print str(i) +":  "+ string + "\n"  
			i=i+1
		# print "which path?\n"+'\n'.join(paths)
		number=int(getAnswer("Which path?"))
		if number<=len(paths) and number>0:
			subprocess.call(["open",paths[number-1]],cwd="/Users/"+name)
		else:
			say("Index out of range")
#====================================
#STUDY BUDDY=========================
def studyBuddy(subject=None):
	if subject==None:
		subject=getAnswer("What subject would you like to go over?")
	data=readJson(studyFile,subject)
	if  data== False:
		if "yes" not in getAnswer("This subject has not been covered, start a new subject?"):
			return 
		else:
			appendJson(studyFile,subject,{})
	say("Teach me")
	com="c"
	while  com=="c":
		key=getAnswer("Question: ")
		value=getAnswer("Answer: ")
		appendJson(studyFile,key,value,subject)
		com=getAnswer("c to continue")
		
def viewSubject(subject):
	# try:
		with open(studyFile) as data_file:
			data = json.load(data_file)
		template = "{0:40}{1:40}"
		data=data[subject]
		for x in data:
			print template.format(x,data[x])
	# except:
	#  	return False

#====================================		

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
		if len(command)==2:
			if command[1]!="stock":
				stock=command[1]
			else:
				stock=command[0]
		else:
			stock=getAnswer("What stock would you like to research?").encode('ascii','ignore')
		say(getStockData(stock))
		subprocess.call(["open","http://stocktwits.com/symbol/"+stock])
	elif "settings" in command and len(command)==1:
		changeDefaultSettings()
	
	elif "ls" in command:
		template = "{0:20}{1:20}{2:20}"
		print template.format("Variable","Current","Options")
		print template.format("Loud:",str(loud),"True, False")
		print template.format("Connected:",str(connected),"True, False")
		print template.format("User:",str(user),"exampleUser")+"\n"
	
	elif "open" in command:
		if len(command)==2:
			grabFile(command[1])
		else:
			grabFile(getAnswer("What file would you like to open?"))
		#build reload command 
	
	elif "openb" in command:
		subprocess.call(["open",command[1]])
	
	elif "clear" in command:
		subprocess.call("clear")

	elif "edit" in command and "commands" in command:
		editCommands()

	elif "google" in command and "open" not in command:
		search=""
		word=""
		for word in command:
			if word!="google":
				search=search+" "+word
		subprocess.call(["open","http://www.google.com/search?q="+search])
	
	elif "read" == command[0]:
		if len(command)==2:
			location=grabFile(command[1])
		else:
			location=grabFile(getAnswer("What file would you like to read?"))
		with open(location) as f:
			for line in f:
				try:
					say(line.rstrip('\n'))
				except:
					pass

	elif "study" in command:
		if len(command)==1:
			studyBuddy()
		else:
			studyBuddy(command[1])
	elif "localsettings" == command[0]:
		setLocalSettings(command[1],command[2])

	elif "help" in command:
		template = "{0:10}{1:30}"
		print template.format("Command","Meaning")
		print template.format("ls","List all current settings for JAX")
		print template.format("open","Open any file")
		print template.format("stock","Get information on any stock")
		print template.format("settings","Change default settings of JAX. Will take effect immediately.")

#==========================

def startup(louds=None,connecteds=None,users=None):
	

	global loud
	global connected
	global user
	getDefaultSettings()
	if louds!=None:
		loud=louds
	if connecteds!=None:
		connected=connecteds
	if users!=None:
		user=users
	
	userInput=""
	while userInput!="quit()" and userInput!="quit":
		userInput=getAnswer("Command")
		jsonifyCommand(userInput)


#Startup processes 
print("Type jax.startup(loud,connected,user)")
#startup()
