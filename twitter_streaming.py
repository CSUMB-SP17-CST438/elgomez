from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

import os  
import json
import flask
import random

import requests
import json
from boto.s3.connection import S3Connection



#Variables that contains the user credentials to access Twitter API 
access_token = os.environ['access_token_twitter']
access_token_secret = os.environ['tokenSecret']
consumer_key =  os.environ['consumer_key_twitter']
consumer_secret = os.environ['consumer_secret_twitter']



class StdOutListener(StreamListener):
    
   ## def on_data(self, data):
       # print data
        #return True
    def on_status(self, status):
        print(status.text)
    
    def on_error(self, status):
        print status


	
app = flask.Flask(__name__)

@app.route('/')
def index():
      #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    stream = Stream(auth, l)
    
    alltweets = []
    alltweets2 = []

    
    new_tweets = api.user_timeline(screen_name = "USPresQuotes",count=200)
    trump_tweets = api.user_timeline(screen_name = "DonaldJTrumpQ",count=200)
    alltweets2.extend(trump_tweets)
    alltweets.extend(new_tweets)
    
    oldest = alltweets[-1].id - 1
    
    while len(new_tweets) > 4000:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = "USPresQuotes",count=200,max_id=oldest)
		trump_tweets = api.user_timeline(screen_name = "DonaldJTrumpQ",count=200,max_id=oldest)
	
		#save most recent tweets
		alltweets.extend(new_tweets)
		alltweets2.extend(trump_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		oldest = alltweets2[-1].id - 1
	
		
  
    r1 = random.randint(1, 2) 
    if r1 == 1:
        n = random.randint(1, len(alltweets))
        string = alltweets[n].text + "\nUser:USPresQuotes\n" + "\nSource: https://twitter.com/statuses/" + str(alltweets[n].id)
    else:
        n2 = random.randint(1, len(alltweets))
        string = alltweets2[n2].text + "\nUser:DonaldJTrumpQ\n" + "\n Source: https://twitter.com/statuses/" + str(alltweets2[n2].id)
    
    url =  "https://api.gettyimages.com/v3/search/images?page_size230,fields=id,title,comp,referral_destinations&sort_order=best&phrase=patriotic"

    my_headers = {
        "Api-key": os.getenv("getty_Api")
        
    }
    
    response = requests.get(url, headers=my_headers)
    json_body = response.json()
    #print (json_body)
    
    #print json.dumps(json_body,indent = 2)
    #print json_body["images"][10]["display_sizes"][0]["uri"]
    urls  = []
    for i in range (0,30):
        urls.append(json_body["images"][i]["display_sizes"][0]["uri"])
    
    print len(urls)
    u =  urls[random.randint(1, len(urls))]
    print u
    
    return flask.render_template("Home.html",r = string,u = u)
    
    
   
@app.route('/template')
def temp():
   return flask.render_template("template.html")

    


app.run(
 port=int(os.getenv('PORT', 8080)),
 host=os.getenv('IP', '0.0.0.0'),
 debug = True
)

