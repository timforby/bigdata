import sys
import argparse
from pyspark import SparkContext, SparkConf

# Setting up context
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
	lines = scvar.map(lambda x: x.split(string)[int(after)].replace('.', "")) #remove period
	return lines
#returns a scvar with only values that contain the string string
def lineswith(scvar, string):
	lines = scvar.filter(lambda x: string.lower() in x.lower()) #case insensitve
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
#returns only keys
def getkey(svar):
	key = svar.map(lambda x: x[0])
	return key


#################### QUESTION METHODS #######################

def uniqueuser(scvar):
	ans = getkey(count(words((cut(lineswith(scvar,"Starting Session"),"of user")))))
	return ans

#replaces keys with values in a string
def replace(line, dict):
	for i,j in dict.items():
		line = line.replace(i, j)
	return line



#################### PARSING #######################


ar = argparse.ArgumentParser()
ar.add_argument("-q", "--question", nargs = '*', required = True, help = "Please enter qestion number followed by host name/s")
args = vars(ar.parse_args())
args = args["question"]
#not tested but coded to work with multiple hosts
question,hosts = args[0],args[1:3]
if len(hosts) < 2:
	print("Please enter atleast two hosts")

#question number print
print("*Q"+str(question)+": ", end="")

#question 1
if int(question) == 1:
	print("line counts")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = str(numlines(readhost(i)))
		print(ans)
#question 2
if int(question) == 2:
	print("sessions of user 'achille'")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = str(numlines(lineswith(lineswith(readhost(i),"Starting Session"),"of user achille")))
		print(ans)
#question 3
if int(question) == 3:
	print("unique user names")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = uniqueuser(readhost(i))
		print(ans.collect())
#question 4
if int(question) == 4:
	print("sessions per user")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = count(words((cut(lineswith(readhost(i),"Starting Session"),"of user"))))
		ans = ans.sortByKey(False)
		print(ans.collect())
#question 5
if int(question) == 5:
	print("number of errors ")
	for i in hosts:
		print(" + "+i+": ", end="")
		ans = str(numlines(lineswith(readhost(i),"error")))
		print(ans)
#question 6
if int(question) == 6:
	print("number of errors ")
	for i in hosts:
		print(" + "+i+": ")
		ans = lineswith(readhost(i),"error").map(lambda x: x[(17+len(str(i))):])
		#cutting at date = 17chars +length of host name
		#count = (lines, #times) -> sort by #times then swap
		ans = swap(count(ans).sortBy(lambda x: x[1], False)).take(5)
		for a in ans:
			print(a)
#question 7
if int(question) == 7:
	print("users who started a session on all hosts ")
	print(" + : ", end="")
	#empty RDD to hold intersections
	fu = uniqueuser(readhost(hosts[0]))
	for i in hosts[1:]:
		fu = fu.intersection(uniqueuser(readhost(i)))
	print(fu.collect())
#question 8
if int(question) == 8:
	print("users who started a session on exactly one host, with host name ")
	print(" + : ", end="")
	fu = sc.emptyRDD()
	for i in hosts:
		#map with host name
		fu = fu.union(uniqueuser(readhost(i)).map(lambda x: (x,i)))
	#repeats will have username, host1+host2+... and thus will not have single host
	print(fu.reduceByKey(lambda x,y: x+y).filter(lambda x: x[1] in hosts).sortBy(lambda x: x[1]).collect())

#question 9
if int(question) == 9:
	print("Host Anonymization")
	for i in hosts:
		print(" + "+i+": ")
		print(" . User name mapping: ", end="")
		us = readhost(i)
		#sort alphabetically, then zipp with its index then prepend user to index
		mapping = uniqueuser(us).sortBy(lambda x: x).zipWithIndex().map(lambda x: (x[0],"user-"+str(x[1])))
		#broadcast dictionary of mapped users
		map_bc = sc.broadcast(mapping.collectAsMap())
		#replace all users using dictionary
		rewrite = us.map(lambda x: replace(x,map_bc.value))
		saveloc = str("data/"+i+"_anonymized")
		rewrite.saveAsTextFile(saveloc)
		print(mapping.collect())
		print(" . Anonymized files: "+saveloc)
