from pyspark import SparkContext
import csv

import os
os.environ["SPARK_HOME"] = "/usr/local/spark/"
os.environ["PYSPARK_PYTHON"]="/usr/local/bin/python3"

symptons={"nausea":0, "fever":1}

def split_tweet_and_location(x):
    x=x.split('\t')
    if len(x)==1:
        return x[0], ""
    else:
        return x[0], x[1].split(',')[1].strip() if len(x[1].split(','))==2 else ""

def map_symptons_to_locations(x):
    l=[0 for _ in range(len(symptons))]
    for word in x[0].split(' '):
        if word in symptons:
            l[symptons[word]]+=1
    return x[1], l

def reduce_symptons_to_location(x):
    return x[0], [sum(x) for x in zip(*x[1])]



sc = SparkContext("local", "project")
tweets = sc.textFile("tweets.txt")
tweets_with_location=tweets.map(split_tweet_and_location)
symptons_with_locations=tweets_with_location.map(map_symptons_to_locations)
symptons_with_locations=symptons_with_locations.groupByKey()
symptons_with_locations=symptons_with_locations.map(reduce_symptons_to_location)

for i in symptons_with_locations.collect():
    print(i)