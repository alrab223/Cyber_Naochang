# twitter-stream1.py
import tweepy
from datetime import timedelta
from dotenv import load_dotenv
import os
import csv
import json
from os.path import join, dirname
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
        text = status.text.replace("#ナゴドの記憶を取り戻せ","")
        icon=status.author.profile_image_url.replace("normal","400x400")
        print(user,text,icon)
        if "retweeted_status" in status._json.keys():
            return True
        
        with open("../json/naosuki_count.json", "r") as f:
           dic = json.load(f)
        dic["count"] += 1
        with open("../json/naosuki_count.json", "w") as f:
           json.dump(dic,f,indent=3)
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
stream.filter(track = ["なおすき"])# 指定の検索ワードでフィルタ