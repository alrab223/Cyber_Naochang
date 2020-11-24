import os
import random
import asyncio
import discord
from discord.ext import commands  # Bot Commands Frameworkのインポート
from discord.ext import tasks
import json
import csv
import glob
from libneko import EmbedNavigator
class Idol(commands.Cog):


   def __init__(self, bot):
      self.bot = bot
   

   @commands.command("アイドル検索")
   async def idol_search(self, ctx, name: str):
      with open("Idol.csv") as f:
         text = [row for row in csv.reader(f)]
      for i in text:
         if i[1] == name:
            num = int(i[0])
      if num == None:
         return
      embed = discord.Embed(title=f"{text[num][1]}({text[num][2]})")
      embed.add_field(name="属性", value=f"{text[num][3]}",inline=False)
      embed.add_field(name="年齢", value=f"{text[num][6]}")
      embed.add_field(name="誕生日", value=f"{text[num][4]}/{text[num][5]}")
      embed.add_field(name="出身地", value=f"{text[num][10]}")
      embed.add_field(name="血液型", value=f"{text[num][8]}")
      embed.add_field(name="利き手", value=f"{text[num][9]}")
      embed.add_field(name="趣味", value=f"{text[num][11]}")
      await ctx.send(embed=embed)

   @commands.command("ユニット検索")
   async def unit_search(self, ctx, *args):
      flag = 0
      count=0
      embed1=discord.Embed(description='ユニット名一覧 1')
      embed2 = discord.Embed(description='ユニット名一覧 2')
      embed3 = discord.Embed(description='ユニット名一覧 3')
      embed4 =discord.Embed(description='ユニット名一覧 4')
      pages = [embed1, embed2, embed3, embed4]
      pages2=[]
      pagesj=[False,False,False,False]
      embed = discord.Embed(title="ユニット名一覧")
      with open("json/unit_kai.json", "r",encoding="utf_8_sig") as f:
         dic=json.load(f)
      for i in dic["results"]["bindings"]:
         for j in list(args):    
            if j in i["メンバー"]["value"]:
               flag+=1
            else:
               break
            if flag == len(list(args)):
               if count<6:
                  embed1.add_field(name=i["ユニット名"]["value"], value=i["メンバー"]["value"], inline=False)
                  pagesj[0]=True
               elif count<12:
                  pagesj[1]=True
                  embed2.add_field(name=i["ユニット名"]["value"], value=i["メンバー"]["value"], inline=False)
               elif count < 18:
                  pagesj[2]=True
                  embed3.add_field(name=i["ユニット名"]["value"], value=i["メンバー"]["value"], inline=False)
               else:
                  pagesj[3]=True
                  embed4.add_field(name=i["ユニット名"]["value"], value=i["メンバー"]["value"], inline=False)
               count+=1
         flag = 0
      for i in range(4):
         if pagesj[i] == True:
            pages2.append(pages[i])         
      nav = EmbedNavigator(ctx, pages2)
      nav.start()


   @commands.command("奈緒ルーレット")
   async def nao_roulette(self, ctx):
      msg=await ctx.send(file=discord.File('picture/nao/nao.gif'))
      await asyncio.sleep(5)
      await msg.delete()
      path = "picture/nao/*.jpg"
      num = glob.glob(path)
      await ctx.send(file=discord.File(random.choice(num)))

   @commands.command("肇ルーレット")
   async def hajime_roulette(self, ctx):
      msg=await ctx.send(file=discord.File('picture/hajime/hajime.gif'))
      await asyncio.sleep(5)
      await msg.delete()
      path = "picture/hajime/*.jpg"
      num = glob.glob(path)
      await ctx.send(file=discord.File(random.choice(num)))

         
      
   

       
       


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):

    bot.add_cog(Idol(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
