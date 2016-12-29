import json
import twitter
import markovify
import praw

tkeys = open("config/twitterconfig.json")
tkeys = json.loads(tkeys.read())

api = twitter.Api(consumer_key=tkeys["consumer_key"],
                  consumer_secret=tkeys["consumer_secret"],
                  access_token_key=tkeys["access_token_key"],
                  access_token_secret=tkeys["access_token_secret"])
arand = open("config/rand.txt")
arand = arand.read()

marx = open("config/marx.txt")
marx = marx.read()

rkeys = open("config/redditconfig.json")
rkeys = json.loads(rkeys.read())
reddit = praw.Reddit(client_id=rkeys["client_id"],
                     client_secret=rkeys["client_secret"],
                     user_agent=rkeys["user_agent"])

subreddit=reddit.subreddit('me_irl')
submissions= []
for submission in subreddit.hot(limit=10):
	submissions.append(submission)
comments =[]
for x in submissions:
    for y in x.comments.list():
        comments.append(y)
toMark = ""
for comm in comments:
    try:
        toMark += ' ' + comm.body
    except:
        pass

model = markovify.Text(toMark+' '+arand+' '+marx)
status = api.PostUpdate(model.make_short_sentence(140))
