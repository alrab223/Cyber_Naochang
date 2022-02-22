import asyncio
import csv
import datetime
import glob
import json
import os
import random

import discord
import requests
import urllib3
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from cog.utils.DbModule import DbModule as db
from cog.utils.webhook_control import Webhook_Control


# コグとして用いるクラスを定義。
class Time(commands.Cog, Webhook_Control):

   def __init__(self, bot):
      self.bot = bot
      self.birthday_sned = False
      self.flag = 1
      self.printer.start()
      self.bd_printer2.start()
      self.weather_list = []
      self.event = False  # 特殊イベントの時のみTrue
      self.db = db()

   def weather_get(self):
      self.weather_list = []
      tokyo = 'https://weather.yahoo.co.jp/weather/jp/13/4410.html'
      osaka = "https://weather.yahoo.co.jp/weather/jp/27/6200.html"
      hokkaido = "https://weather.yahoo.co.jp/weather/jp/1b/1400.html"
      hukuoka = "https://weather.yahoo.co.jp/weather/jp/40/8210.html"
      weather_lists = [tokyo, osaka, hokkaido, hukuoka]
      name = ["東京", "大阪", "北海道", "福岡"]
      http = urllib3.PoolManager()
      for i, j in enumerate(weather_lists):
         instance = (http.request('GET', j))
         soup = BeautifulSoup(instance.data, 'html.parser')
         tenki_today = soup.select_one('#main > div.forecastCity > table > tr > td > div > p.pict')
         try:
            text = tenki_today.text.replace("今日の天気は", "")
            self.weather_list.append(f"{name[i]}の天気:{text}")
         except AttributeError:
            pass

   @commands.command("天気取得")
   async def test_reset(self, ctx):
      self.weather_get()

   async def get_webhook(self, channel):
      while True:
         ch_webhooks = await channel.webhooks()
         webhook = discord.utils.get(ch_webhooks, name="naochang")
         if webhook is None:
            await channel.create_webhook(name="naochang")
         else:
            return webhook

   @commands.command("b4")
   async def stamp66(self, ctx, *emojis: discord.Emoji):
      url = 'https://discord.com/'
      embeds = []
      for emoji in emojis:
         embeds.append(discord.Embed(url=url).set_image(url=emoji.url))
      wh = discord.utils.get(await ctx.channel.webhooks(), name='久川颯')
      await ctx.message.delete()
      await wh.send(embeds=embeds, username=ctx.author.display_name, avatar_url=ctx.message.author.avatar_url_as(format="png"))

   @tasks.loop(seconds=5.0)
   async def bd_printer2(self):
      if self.flag == 1:
         count = self.db.select('select count from naosuki_count')[0]
         text = "なおすきカウント:" + str(count["count"])
         await self.bot.change_presence(activity=discord.Game(name=text))
         self.flag += 1
      elif self.flag == 2:
         try:
            await self.bot.change_presence(activity=discord.Game(name=self.weather_list[0]))
            num = self.weather_list.pop(0)
            self.weather_list.append(num)
         except IndexError:
            pass
         self.flag += 1
      else:
         guild = self.bot.get_guild(int(os.environ.get("FotM")))
         user_count = sum(1 for member in guild.members if not member.bot)
         await self.bot.change_presence(activity=discord.Game(name=f"現在のメンバー数:{user_count-4}"))
         self.flag = 1

   @bd_printer2.before_loop
   async def before_printer(self):
      print('waiting...')
      await self.bot.wait_until_ready()
      url = "https://starlight.kirara.ca/api/v1/list/card_t"
      r = requests.get(url).json()
      with open("json/idol_data.json", "w")as f:
         json.dump(r, f, indent=3)
      print('データベースを更新しました')

   @tasks.loop(seconds=6.0)
   async def printer3(self):
      channel = self.bot.get_channel(int(os.environ.get("")))  # 垂れ流し先のチャンネル
      print("開始")
      with open("text/global_stream.csv") as f:
         reader = csv.reader(f)
         l = [row for row in reader]
         l = l[-3:]
      for _ in range(3):
         if os.path.getsize("text/global_stream.csv") > 0:
            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name="naochang")
            try:
               await webhook.send(content=l[0][1],
                                  username=l[0][0],
                                  avatar_url=l[0][2])
               del l[0]
            except discord.errors.HTTPException:
               del l[0]
               pass
            except IndexError:
               pass
      with open("text/global_stream.csv", "w") as f:
         writer = csv.writer(f)
         writer.writerows(l)

   @tasks.loop(seconds=60.0)
   async def printer(self):
      nowtime = datetime.datetime.now()
      if nowtime.hour == 23 and nowtime.minute == 59:
         wait_seconds = 60.0 - float(nowtime.second)
         await asyncio.sleep(wait_seconds)
         if self.event:
            await self.special_daily()
         self.db.update('update user_data set mayuge_coin=mayuge_coin+3,naosuki=0')
         self.weather_get()
         channel = self.bot.get_channel(int(os.environ.get("naosuki_ch")))
         path = "picture/nao/*.jpg"
         num = glob.glob(path)
         await channel.send(file=discord.File(random.choice(num)))
         await channel.send("まゆげコインを追加しました")
         await channel.send("今日も1日なおすき！！")
         emoji = ""
         with open("json/emoji.json", "r")as f:
            dic = json.load(f)
         for i in dic["rainbow_art"]:
            emoji += str(self.bot.get_emoji(int(i)))
         await channel.send(emoji)
         nowtime = datetime.datetime.now()  # 予約投稿用にもう一度時刻取得

      messages = self.db.select("select * from future_send")
      for message in messages:
         if message['time'] == f"{nowtime.year}/{nowtime.month}/{nowtime.day}-{nowtime.hour}:{str(nowtime.minute).zfill(2)}":
            user = await self.bot.fetch_user(message['id'])
            channel = self.bot.get_channel(message['channel_id'])
            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name="naochang")
            if webhook is None:
               await channel.create_webhook(name="naochang")
               ch_webhooks = await channel.webhooks()
               webhook = discord.utils.get(ch_webhooks, name="naochang")
            await webhook.send(content=message['text'],
                               username=user.name,
                               avatar_url=user.avatar_url_as(format="png"))
            self.db.update(f"delete from future_send where time='{message['time']}' and id={message['id']}")

def setup(bot):
   bot.add_cog(Time(bot))
