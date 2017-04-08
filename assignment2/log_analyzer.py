import sys
import argparse
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("wordcount").setMaster("local")
sc = SparkContext(conf=conf)

#################### GENERAL METHODS #######################

#reads the lines of a given host
def readhost(host):
	lines = sc.textFile("data/"+host+"/part-0000*")
	return lines

#returns the number of a specific sc var
def numlines(scvar):
	count = scvar.count()
	return count
#cuts values in scvar after or before a certain string
def cut(scvar,string,after=True):
	lines = scvar.map(lambda x: x.split(string)[int(after)].replace('.', ""))
	return lines
#returns a scvar with only values that contain the string string
def lineswith(scvar, string):
	lines = scvar.filter(lambda x: string.lower() in x.lower())
	return lines

#counts all values in scvar
def count(scvar):
	lines = scvar.map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y)
	return lines

# flatten to words
def words(scvar):
	words = scvar.flatMap(lambda x: x.split())
	return words

#take key values and swap them
def swap(scvar):
	swapped = scvar.map(lambda k: (k[1],k[0]))
	return swapped

def getkey(svar):
	key = svar.map(lambda x: x[0])#cleanup .
	return key
#################### QUESTION METHODS #######################

def uniqueuser(i):
	ans = getkey(count(words((cut(lineswith(readhost(i),"Starting Session"),"of user")))))
	return ans




#################### PARSING #######################


ar = argparse.ArgumentParser()
ar.add_argument("-q", "--question", nargs = '*', required = True, help = "Please enter qestion number followed by host name/s")
args = vars(ar.parse_args())
args = args["question"]
question,hosts = args[0],args[1:3]

print("*Q"+str(question)+": ", end="")

if int(question) == 1:
	print("line counts")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = str(numlines(readhost(i)))
		print(ans)

if int(question) == 2:
	print("sessions of user 'achille'")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = str(numlines(lineswith(lineswith(readhost(i),"Starting Session"),"of user achille")))
		print(ans)

if int(question) == 3:
	print("unique user names")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = uniqueuser(i)
		print(ans.collect())

if int(question) == 4:
	print("sessions per user")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = count(words((cut(lineswith(readhost(i),"Starting Session"),"of user"))))
		ans = ans.map(lambda x: (x[0].replace('.', ""),x[1]))#cleanup .
		ans = ans.sortByKey(False).collect()
		print(ans)

if int(question) == 5:
	print("number of errors ")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = str(numlines(lineswith(readhost(i),"error")))
		print(ans)

if int(question) == 6:
	print("number of errors ")
	for i in hosts:
		print(" + "+i+": ")
		ans = lineswith(readhost(i),"error").map(lambda x: x[(17+len(str(i))):])
		ans = swap(count(ans)).sortByKey(False)
		ans = ans.collect()
		for a in ans[:5]:
			print(a)

if int(question) == 7:
	print("users who started a session on all hosts ")
	print(" + : ", end="")
	fu = sc.emptyRDD()
	for i in hosts:
		fu = fu.intersection(uniqueuser(i))
	print(fu.collect())

if int(question) == 8:
	print("users who started a session on exactly one host, with host name ")
	print(" + : ", end="")
	fu = sc.emptyRDD()
	for i in hosts:
		fu = fu.union(uniqueuser(i).map(lambda x: (x,i)))
	print(fu.reduceByKey(lambda x,y: x+y).filter(lambda x: x[1] in hosts).collect())

if int(question) == 9:
	for i in hosts:
		us = uniqueuser(i)
		