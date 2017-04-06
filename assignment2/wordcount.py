import sys
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("wordcount").setMaster("local")
sc = SparkContext(conf=conf)

in_f = "test.txt"
ou_f = "out"

counts = sc.textFile(in_f).flatMap(lambda x: x.split()).map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y)

counts.saveAsTextFile(ou_f)
