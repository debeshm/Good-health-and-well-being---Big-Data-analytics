from pyspark import SparkContext
import csv

import os
os.environ["SPARK_HOME"] = "/usr/local/spark/"
os.environ["PYSPARK_PYTHON"]="/usr/local/bin/python3"

symptom_list=["pain","pressure","squeezing","chest pain","discomfort","shortness of breath","cold sweat","nausea","lightheadedness",\
"arm weaknes","dizziness","loss of vision","confusion","severe headache","bleeding","itching","burning","frequent urination"\
,"nipple discharge","breast tenderness","skin changes","cough","pneumonia","wheezing","constipation","diarrhea"\
,"vomiting","flushing","redness","jaundice","muscle pain","numbness","stiffness","swelling","inflammation","anxiety","depression"\
,"nightmares","hallucinations","starvation","dehydration"]

symptons={}
i=0
for s in symptom_list:
    symptons[s]=i
    i+=1

print(symptons)

def split_tweet_and_location_with_date(x):
    x=x.split('\t')
    # return as tweet, location, date
    print(len(x))
    if len(x)==2:
        return x[0], '', x[1]
    else:
        return x[0], x[1].split(',')[1].strip().upper() if len(x[1].split(','))==2 else "", x[2]

def map_symptons_to_locations_and_year_month(x):
    l=[0 for _ in range(len(symptons))]
    for word in x[0].split(' '):
        if word in symptons:
            l[symptons[word]]+=1
    return (x[1], x[2]), l

def reduce_symptons_to_location(x):
    return x[0], [sum(x) for x in zip(*x[1])]

sc = SparkContext("local", "project")
tweets = sc.textFile("tweets_latest.txt")
tweets_with_location=tweets.map(split_tweet_and_location_with_date)
symptons_with_locations_and_year_month=tweets_with_location.map(map_symptons_to_locations_and_year_month)
symptons_with_locations_and_year_month=symptons_with_locations_and_year_month.groupByKey()
symptons_with_locations=symptons_with_locations_and_year_month.map(reduce_symptons_to_location)

for i in symptons_with_locations.collect():
    print(i[0], list(i[1]))