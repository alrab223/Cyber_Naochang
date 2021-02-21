# twitter-stream1.py
import tweepy
from datetime import timedelta
from dotenv import load_dotenv
import os
import csv
import random
from os.path import join, dirname
import cv2
import requests
import tempfile
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
CK = os.environ.get("CK")
CS = os.environ.get("CS")
AT = os.environ.get("AT")
AS = os.environ.get("AS")

# StreamListenerを継承するクラスListener作成


class Listener(tweepy.StreamListener):

   def imread_web(self, url):
    # 画像をリクエストする
      res = requests.get(url)
      img = None
      # Tempfileを作成して即読み込む
      with tempfile.NamedTemporaryFile(dir='./') as fp:
         fp.write(res.content)
         fp.file.seek(0)
         img = cv2.imread(fp.name)
      return img

   def on_status(self, status):
      status.created_at += timedelta(hours=9)  # 世界標準時から日本時間に
      print('------------------------------')
      user = status.author.name
      text = status.text.replace("#アイマス三昧", "")
      icon = status.author.profile_image_url.replace("normal", "400x400")

      if "retweeted_status" in status._json.keys() or "RT" in text:
         return True
      # if random.randint(1, 2) != 1:#対象が多いときの対策
      #     return True
      if hasattr(status, 'extended_entities'):  # statusが'extended_entities'属性を持っているか判定
         ex_media = status.extended_entities['media']
         tweet_id = status.id
         if 'video_info' in ex_media[0]:
            ex_media_video_variants = ex_media[0]['video_info']['variants']
            media_name = '%s-%s.mp4' % ("alb", tweet_id)
            if 'animated_gif' == ex_media[0]['type']:
               # GIFファイル
               gif_url = ex_media_video_variants[0]['url']

            else:
               # 動画ファイル
               bitrate_array = []
               for movie in ex_media_video_variants:
                  bitrate_array.append(movie.get('bitrate', 0))
               max_index = bitrate_array.index(max(bitrate_array))
               movie_url = ex_media_video_variants[max_index]['url']

         else:
            # 画像ファイル
            for image in ex_media:
               image_url = image['media_url']
               img = self.imread_web(image_url)
               cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
               cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
               cv2.imshow("screen", img)
               cv2.waitKey(5000)

      #   with open("../text/global_stream.csv", "a") as f:
      #      print(text)
      #      writer = csv.writer(f)
      #      writer.writerow([user,text,icon])
      #   return True

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
stream.filter(track=["#シンデレラHNYリモート名刺交換会"])  # 指定の検索ワードでフィルタ
