from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd
import tweepy as tw

#Variables that contains the user credentials to access Twitter API 

access_token = "1122647574584942594-4OgoWq56fOouYUe9wEmCAlAGleIyXA"
access_token_secret = "4w4RnDO297eYPshVgvkX66r3mkCP1nbw3uUl2lG2dZuDb"
consumer_key = "SQT6mS0nRfDCfIQRYi3lVrDGh"
consumer_secret = "ZQxgUtkEacSqjz25Jwo0REWp8Zk8y1hmYX9SOFKcEPheh9Mpvp"

'''
access_token = "2921481343-MG0KQdBMqQ609bCVQHrfBdorou2lzzPT0ycWDNL"
access_token_secret = "a16odt2c4klr6JTMKI9euV10287Bb2F74xUIW2jWwrIbx"
consumer_key = "UOG0ObA7y0iXXZwB6UYD5yPtk"
consumer_secret = "0Vq83yEqu0L1auw58hCaqwVDQte1Cx6L0aRvaRMuu7uhEoigK4"
'''

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    #stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])
    #stream.filter(track=['#digitalhealth'])

    api = tw.API(auth, wait_on_rate_limit=True)
    search_words = "chest pain"
    date_since = "2016-04-20"


    symptom_list=["nightmares","hallucinations","starvation","dehydration"]

    for s in symptom_list:

        search_words=s

        tweets = tw.Cursor(api.search,
                q=search_words,
                lang="en"
                ).items(2000)
        #print(len(list(tweets)))
        f= open("tweets_latest.txt","a+")
        #for i in list(filter(lambda x: "new york" in x.user.location.lower(), tweets)):
        j=0
        for i in tweets:
            #print(i.text, i.user.location)
            #print("\n")
            f.write(i.text.replace('\n', '') + "\t" + i.user.location + "\t" + str(i.user.created_at) + "\n")
            print(s + str(j) + i.text.replace('\n', '') + "\t" + i.user.location + "\t" + str(i.user.created_at) + "\n")
            j+=1
        
        f.close() 
        print(j)