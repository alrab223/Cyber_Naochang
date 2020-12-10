from discord.ext import commands,tasks  # Bot Commands Frameworkのインポート
import datetime
import json
import os
import discord
import subprocess
import shutil
import csv
import random
import glob
import sqlite3
import urllib3
from bs4 import BeautifulSoup
# コグとして用いるクラスを定義。
class Time(commands.Cog):

   wait_seconds = 60.0   
   def __init__(self, bot):
       self.bot = bot
       self.birthday_sned = False
       self.preurl = []
       self.flag=1
       self.printer.start()
       self.bd_printer2.start()
       self.weather_list = []
       with open("text/idol.txt", "r") as f:
          self.idol_command=f.read().replace("\n","")
       
       
   
   def daily_reset(self):
      with (sqlite3.connect("db/bot_data.db")) as conn:
         c = conn.cursor()
         sql = c.execute(f'select id from userdata where vc_notification=0')
         id_list = [x[0] for x in sql]
         for i in id_list:
            c.execute(f'update userdata set mayuge_coin=mayuge_coin+3,naosuki=0 where id={i}')
         conn.commit()
   
   def weather_get(self):
      self.weather_list=[]
      tokyo = 'https://weather.yahoo.co.jp/weather/jp/13/4410.html'
      osaka="https://weather.yahoo.co.jp/weather/jp/27/6200.html"
      hokkaido="https://weather.yahoo.co.jp/weather/jp/1b/1400.html"
      hukuoka="https://weather.yahoo.co.jp/weather/jp/40/8210.html"
      weather_lists=[tokyo,osaka,hokkaido,hukuoka]
      name=["東京","大阪","北海道","福岡"]
      http = urllib3.PoolManager()
      for i ,j in enumerate(weather_lists):
         instance=(http.request('GET', j))
         #instanceからHTMLを取り出して、BeautifulSoupで扱えるようにパースします
         soup = BeautifulSoup(instance.data, 'html.parser')
         #CSSセレクターで天気のテキストを取得します。
         #今日の天気
         tenki_today = soup.select_one('#main > div.forecastCity > table > tr > td > div > p.pict')
         text=tenki_today.text.replace("今日の天気は","")
         self.weather_list.append(f"{name[i]}の天気:{text}")
   
   async def daily_idol(self,channel):
      with (sqlite3.connect("db/bot_data.db")) as conn:
            c = conn.cursor()
            c.execute(f'select *from idol_data where done!=1')
            idol = c.fetchall()
            idol=random.choice(idol)
            with open("text/idol.txt", "w") as f:
               f.write(idol[0])
            num = random.randint(1, 5)
            await channel.send("今日のアイドル")
            if num==1:
               await channel.send(f"誕生日が{idol[1]}、趣味が「{idol[7]}」のアイドルは...")
            elif num == 2:
               await channel.send(f"誕生日が{idol[1]}、属性{idol[2]}、{idol[5]}出身のアイドルは...")
            elif num == 3:
               await channel.send(f"誕生日が{idol[1]}、{idol[3]}歳、{idol[5]}出身のアイドルは...")
            elif num == 4:
               await channel.send(f"誕生日が{idol[1]}、{idol[4]}型、{idol[5]}出身のアイドルは...")
            else:
               await channel.send(f"趣味が「{idol[7]}」のアイドルは...")
            await channel.send(f"```!今日のアイドル アイドル名```")
            
            conn.commit()
            self.idol_command=idol[0]
         
         
         

   
   @commands.command("天気取得")
   async def test_reset(self, ctx):
      self.weather_get()
   
   @commands.command("てすとず")
   async def test_idol(self, ctx):
      channel = self.bot.get_channel(744610643927236750)
      await self.daily_idol(channel)
   
   @commands.command("今日のアイドル")
   async def today_idol(self, ctx, name: str):
      channel = self.bot.get_channel(744610643927236750)
      if ctx.channel.id != 744610643927236750:
         return
      if name == self.idol_command:
         
         await channel.send("当たり！")
         with (sqlite3.connect("db/bot_data.db")) as conn:
            c = conn.cursor()
            c.execute(f'select *from idol_data where name="{self.idol_command}"')
            idol = c.fetchall()[0]
            tall=idol[10]
            embed = discord.Embed(title=f"{idol[0]}")
            files = discord.File(f"picture/daily_idol/{self.idol_command}.png", filename="image.png")
            embed.set_image(url="attachment://image.png")
            embed.add_field(name="属性", value=f"{idol[2]}",inline=False)
            embed.add_field(name="年齢", value=f"{idol[3]}")
            embed.add_field(name="身長", value=f"{tall}")
            embed.add_field(name="誕生日", value=f"{idol[1]}")
            embed.add_field(name="出身地", value=f"{idol[5]}")
            embed.add_field(name="血液型", value=f"{idol[4]}")
            embed.add_field(name="利き手", value=f"{idol[6]}")
            embed.add_field(name="趣味", value=f"{idol[7]}")
            embed.add_field(name="奈緒との身長差", value=f"{tall-154}")
            await ctx.send(file=files, embed=embed)
            c.execute(f'update idol_data set done=1 where name="{idol[0]}"')
            conn.commit()
         with open("text/idol.txt", "w") as f:
            f.write("noncommand_commands")
         self.idol_command = "noncommand_commands"
      
      elif self.idol_command == "noncommand_commands":
         pass
      else:
         await channel.send("残念！")
         
      
   
   @commands.command("")
   async def start3(self, ctx):
      self.printer3.start()
         
   @tasks.loop(seconds=6.0)
   async def printer2(self):
      channel = self.bot.get_channel()
      with open("src/stream.txt", "r") as f:
         tweet = f.read().splitlines()
      if os.path.getsize("src/stream.txt") > 0:
         await channel.send(tweet[0])
         del tweet[0]
         with open("src/stream.txt", "w") as f:
            f.write("\n".join(tweet))
   
   @tasks.loop(seconds=5.0)
   async def bd_printer2(self):
      if self.flag==1:
         with open("json/naosuki_count.json")as f:
            dic = json.load(f)
         text="なおすきカウント:"+str(dic["count"])
         await self.bot.change_presence(activity=discord.Game(name=text))
         self.flag+=1
      elif self.flag == 2:
         try:
            await self.bot.change_presence(activity=discord.Game(name=self.weather_list[0]))
            num=self.weather_list.pop(0)
            self.weather_list.append(num)
         except IndexError:
            pass
         self.flag+=1
      else:
         guild=self.bot.get_guild(566227588054253569)
         user_count = sum(1 for member in guild.members if not member.bot)
         await self.bot.change_presence(activity=discord.Game(name=f"現在のメンバー数:{user_count-4}"))
         self.flag=1
   
   @tasks.loop(seconds=6.0)
   async def printer3(self):
    
      channel = self.bot.get_channel(778607627667898398)
      print("開始")
      with open("text/global_stream.csv") as f:
         reader = csv.reader(f)
         l = [row for row in reader]
         l=l[-3:]
      for _ in range(3):
         if os.path.getsize("text/global_stream.csv") > 0:
            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name="naochang")
            try :
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
   
   @tasks.loop(seconds=6.0)
   async def printer4(self):
    
      channel = self.bot.get_channel(778607627667898398)
      print("開始")
      with (sqlite3.connect("src/tweet.db")) as conn:
         c = conn.cursor()
         c.execute(f'select count(*) from tweet')
         count_record:int = c.fetchall()[0][0]
         for _ in range(3):
            if count_record > 0:
               c.execute(f'select name,text,icon from tweet')
               l = c.fetchall()
               ch_webhooks = await channel.webhooks()
               webhook = discord.utils.get(ch_webhooks, name="naochang")
               try :
                  await webhook.send(content=l[1][0],
                        username=l[0][0],
                        avatar_url=l[2][0])
               except discord.errors.HTTPException:
                  pass
            c.execute("delete from tweet where num=(select min(num) from tweet)")

   @bd_printer2.before_loop
   async def before_printer(self):
      print('waiting...')
      await self.bot.wait_until_ready()
   
   
   @tasks.loop(seconds=wait_seconds)
   async def printer(self):
    
      nowtime = datetime.datetime.now()
      if nowtime.hour == 0 and nowtime.minute == 0 :
         self.daily_reset()
         self.weather_get()
         channel = self.bot.get_channel(744610643927236750)
         path = "picture/nao/*.jpg"
         num = glob.glob(path)
         await channel.send(file=discord.File(random.choice(num)))
         await channel.send("まゆげコインを追加しました")
         await channel.send("今日も1日なおすき！！")
         emoji=""
         with open("json/emoji.json", "r")as f:
            dic=json.load(f)
         for i in dic["rainbow_art"]:
            emoji += str(self.bot.get_emoji(int(i)))
         await channel.send(emoji)
         Time.wait_seconds = 60.0
         await self.daily_idol(channel)

      elif nowtime.hour == 23 and nowtime.minute == 59:
         Time.wait_seconds = 60.0- float(nowtime.second)
         

    
# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Time(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
