import tweepy
import datetime
import os
from dotenv import load_dotenv
import schedule
from pytz import timezone
import random
import time
import sys


load_dotenv()
tz = timezone('Asia/Tokyo')


Consumer_key = os.environ['CONSUMER_API_KEY'] 
Consumer_secret = os.environ["CONSUMER_API_SECRET_KEY"]
Bearer_token = os.environ["BEARER_TOKEN"]
Access_token = os.environ["ACCESS_TOKEN"]
Access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]


client = tweepy.Client(
  bearer_token = Bearer_token,
	consumer_key = Consumer_key,
	consumer_secret = Consumer_secret,
	access_token = Access_token,
	access_token_secret = Access_token_secret
)


count = int(input("ツイート回数を入力してください->"))
foods = ["ハンバーグ","カレー","アイス","寿司","牛丼","ラーメン","焼肉","パフェ","うどん","スパゲッティ","ピザ","唐揚げ"]
tweet_contents = []
i = 0


class Message():
  def __init__(self,foods):
    self.order_num = random.randrange(len(foods))
    self.randomfood = foods[self.order_num]


  def greet(self,time):
    if 4 < time.hour < 12:
      self.greet = "おはよう！"
    elif 12 < time.hour < 18:
      self.greet = "こんにちは！"
    else:
      self.greet = "こんばんは！"

    self.message = f"{self.greet}世界。もう{time.hour}時{time.minute}分だね～。{self.randomfood}が食べたいな。"
    return self.message


for num in range(count):
  tweet_contents.append(Message(foods))


def tweet(content):
  global i
  curent_time = datetime.datetime.now(tz)
  post = content[i].greet(curent_time)
  response = client.create_tweet(text=post)
  print(response)
  i += 1


schedule.every(1).minutes.at(":00").do(tweet,tweet_contents)


while True:
  if i >= len(tweet_contents):
    sys.exit()
  schedule.run_pending()
  time.sleep(1)


