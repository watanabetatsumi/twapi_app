import tweepy
import datetime
import os
from dotenv import load_dotenv
import schedule
from pytz import timezone
import random
import time
import sys

# タイムゾーンの指定
tz = timezone('Asia/Tokyo')

# 環境変数から、APIキー等を取得
load_dotenv()
Consumer_key = os.environ['CONSUMER_API_KEY'] 
Consumer_secret = os.environ["CONSUMER_API_SECRET_KEY"]
Bearer_token = os.environ["BEARER_TOKEN"]
Access_token = os.environ["ACCESS_TOKEN"]
Access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

# クライアントの作成
client = tweepy.Client(
  bearer_token = Bearer_token,
	consumer_key = Consumer_key,
	consumer_secret = Consumer_secret,
	access_token = Access_token,
	access_token_secret = Access_token_secret
)


# メッセージ内容を生成するクラスを作成
class Message():
  def __init__(self):
    self.want_eat()
# 投稿する時間によってあいさつの仕方を変えつつ、メッセージを取得
  def greet(self,time):
    if 4 < time.hour < 12:
      self.greet = "おはよう！"
    elif 12 < time.hour < 18:
      self.greet = "こんにちは！"
    else:
      self.greet = "こんばんは！"

    self.message = f"{self.greet}世界。もう{time.hour}時{time.minute}分だね～。{self.randomfood}が食べたいな。"
    return self.message
  
  # つぶやく内容を少しひねって、時刻情報以外に食べたいものをランダムに投稿するようにする。
  def want_eat(self):
    self.foods = ["ハンバーグ","カレー","アイス","寿司","牛丼","ラーメン","焼肉","パフェ","うどん","スパゲッティ","ピザ","唐揚げ"]
    self.order_num = random.randrange(len(self.foods))
    self.randomfood = self.foods[self.order_num]

# ツイート数の決定
count = int(input("ツイート回数を入力してください->"))

# ツイートを要求分だけ生成
tweet_contents = []
for num in range(count):
  tweet_contents.append(Message())

# ツイート内容を投稿する関数
i = 0
def tweet(contents):
  global i
  current_time = datetime.datetime.now(tz)
  post = contents[i].greet(current_time)
  response = client.create_tweet(text=post)
  print(response)
  i += 1

# ツイートの実行を予約
schedule.every(1).minutes.at(":00").do(tweet,tweet_contents)


while True:
  if i >= len(tweet_contents):
    sys.exit()
  schedule.run_pending()
  time.sleep(1)


