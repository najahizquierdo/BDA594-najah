import pandas as pd
import tweepy
import pymongo

client = pymongo.MongoClient()
database = client['data']
collection = database['tweets']

BEARER_TOKEN: str = 'AAAAAAAAAAAAAAAAAAAAAMkXhwEAAAAAZHz9atPytihf4BIF8rqmEfENGPQ%3DJ8TH3qUAuqPzsuqzHnQNpVQ5aQKKVSztVwLeyzEyqxei6jwyXy'

CLIENT = tweepy.Client(bearer_token=BEARER_TOKEN)

response = CLIENT.search_recent_tweets(query="bunny", max_results=100,
                                        expansions=['author_id'],
                                        tweet_fields=['author_id', 'text', 'public_metrics'],
                                        user_fields=['id', 'name', 'username', 'public_metrics'])
tweets = []
users = []

tweets += [tweet.data for tweet in response[0]]
users += [user.data for user in response.includes['users']]

data = dict()
data['tweet_id'] = [tweet['id'] for tweet in tweets]
data['text'] = [tweet['text'] for tweet in tweets]
data['author_id'] = [tweet['author_id'] for tweet in tweets]
data['tweet_stats'] = [tweet['public_metrics'] for tweet in tweets]

tdf = pd.DataFrame(data)

data = dict()
data['user_id'] = [user['id'] for user in users]
data['user_username'] = [user['username'] for user in users]
data['user_full_name'] = [user['name'] for user in users]
data['user_stats'] = [user['public_metrics'] for user in users]
udf = pd.DataFrame(data)

tdf = tdf.merge(udf, left_on='author_id', right_on='user_id', how='left')
collection.insert_many(tdf.to_dict('records'))
