# twitter-stream1.py
import tweepy
from datetime import timedelta
from dotenv import load_dotenv
import os
import csv
import random
from os.path import join, dirname
import sqlite3
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
CK= os.environ.get("CK") 
CS= os.environ.get("CS") 
AT= os.environ.get("AT") 
AS= os.environ.get("AS") 

 # StreamListenerを継承するクラスListener作成
class Listener(tweepy.StreamListener):
    def on_status(self, status):
        status.created_at += timedelta(hours=9)#世界標準時から日本時間に

        print('------------------------------')
        user = status.author.name
        text = status.text.replace("#アイマス三昧","")
        icon=status.author.profile_image_url.replace("normal","400x400")
        
        if "retweeted_status" in status._json.keys() or "#" in text or "RT" in text:
            return True
        if random.randint(1, 2) != 1:#対象が多いときの対策
            return True
      #   with (sqlite3.connect("tweet.db")) as conn:
      #      c = conn.cursor()
      #      data=[user,text,icon]
      #      c.execute(f'insert into tweet (name,text,icon) values (?,?,?)',data)
      #      conn.commit()
        with open("../text/global_stream.csv", "a") as f:
           print(text)
           writer = csv.writer(f)
           writer.writerow([user,text,icon])        
        return True

    def on_error(self, status_code):
        print('エラー発生: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

 # Listenerクラスのインスタンス
listener = Listener()
# 受信開始
stream = tweepy.Stream(auth, listener)
stream.filter(track = ["アイマス三昧"])# 指定の検索ワードでフィルタ