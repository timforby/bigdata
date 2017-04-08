import sys
import argparse
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("wordcount").setMaster("local")
sc = SparkContext(conf=conf)

#reads the lines of a given host
def readhost(host):
	lines = sc.textFile("data/"+host+"/part-0000[0-4]*")
	return lines

#returns the number of a specific sc var
def numlines(scvar):
	count = scvar.count()
	return count
#cuts values in scvar after or before a certain string
def cut(scvar,string,after=True):
	lines = scvar.map(lambda x: x.split(string)[int(after)])
	return lines
#returns a scvar with only values that contain the string string
def lineswith(scvar, string):
	lines = scvar.filter(lambda x: string in x)
	return lines

#counts all values in scvar
def count(scvar):
	lines = scvar.flatMap(lambda x: x.split()).map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y)
	return lines

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
		ans = count(cut(lineswith(readhost(i),"Starting Session"),"of user"))
		ans = ans.map(lambda x: x[0].replace('.', ""))#cleanup .
		ans = ans.collect()
		print(ans)

if int(question) == 4:
	print("sessions per user")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = count(cut(lineswith(readhost(i),"Starting Session"),"of user"))
		ans = ans.map(lambda x: (x[0].replace('.', ""),x[1]))#cleanup .
		ans = ans.collect()
		print(ans)

if int(question) == 5:
	print("number of errors ")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = str(numlines(lineswith(lineswith(readhost(i),"Starting Session"),"of user achille")))
		print(ans)

