from pyspark import SparkContext
import csv

import os
os.environ["SPARK_HOME"] = "/usr/local/spark/"
os.environ["PYSPARK_PYTHON"]="/usr/local/bin/python3"

sc = SparkContext("local", "project")
tweets = sc.textFile("bd_edited_final.tsv").map(lambda x: x.split('\t'))
'''
l=tweets.take(2)[1]
for i, j in enumerate(l):
    print(i, " ", j)
'''
tweets_filtered=tweets.filter(lambda x: x[34]=='influenza' or x[34]=='hepatitis A')
tweets_filtered=tweets_filtered.map(lambda x: ((x[1], x[34]), 1))
tweets_filtered=tweets_filtered.groupByKey()
counts=tweets_filtered.map(lambda x: (x[0], sum(x[1])))

for i in counts.collect():
    print(i)