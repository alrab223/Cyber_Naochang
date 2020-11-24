from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord
import random
import re
import linecache
import csv
from discord.utils import get
import json
import asyncio
import glob
import os
from dotenv import load_dotenv
import sqlite3
load_dotenv()
# コグとして用いるクラスを定義。
class Game(commands.Cog):


   def __init__(self, bot):
        self.bot = bot
        self.handbattle = False
        self.slot = False
        self.chance=False
   
   def get_emoji(self):
      with open("json/emoji.json", "r")as f:
         emoji = json.load(f)
      return emoji["special"][random.choice(list(emoji["special"].keys()))]
  
   
   @commands.command("じゃんけん")
   async def funny(self, ctx):
      if self.handbattle == True:
         return
      self.handbattle == True
      await ctx.send("じゃんけんしましょう。最初はパー")
      hand = random.randint(0, 2)
      dic={"グー":0,"チョキ":1,"パー":2}
      ch_webhooks = await ctx.channel.webhooks()
      webhook = discord.utils.get(ch_webhooks, name="久川颯")
      await webhook.send(content="せっ……出せっ！！グーチョキパーだ！早くしろ！",
             username="藤原竜也",
             avatar_url="https://stat.ameba.jp/user_images/20150306/19/tamagochan-deddosusi/3f/05/j/t02200220_0354035413237066758.jpg?caw=800")
      def check(m):
         return m.author.id==ctx.author.id and (m.content == 'グー' or m.content == 'チョキ' or m.content == 'パー') and m.channel == ctx.channel
      
      msg = await self.bot.wait_for('message', check=check)
      await ctx.send(f"{list(dic.keys())[hand]}です")
      with open("json/bot_id.json", "r") as f:
         dic2 = json.load(f)
      
      if dic[msg.content] == (hand + 2) % 3:
         await ctx.send("あなたの勝ちです。ねぎどうぞ")
         dic2[str(ctx.author.id)]["gold"] += 300
      elif dic[msg.content] == (hand + 1) % 3:
         await ctx.send("凪の勝ちです。300みつはもらいますね、わーい")
         dic2[str(ctx.author.id)]["gold"] -= 300
      else:
         await ctx.send("引き分けですね")

      with open("json/bot_id.json", "w") as f:
         json.dump(dic2,f,indent=3)
      self.handbattle == False

   @commands.command("")
   async def emoji(self, ctx):
      emoji = await ctx.guild.fetch_emojis()
      for i in emoji:
         print(i)
   
   async def bonus_slot(self, ctx, ei, judge,msg):
      count = 0
      for i, element in enumerate(ei):
         if judge[i] == element:
            count += 1

      if (count == 3 or count==4) and  random.randint(1, 5) == 1:
         self.chance=True
         gif = await ctx.send("チャンス発生！！", file=discord.File("picture/bonus/triad.gif"))
         
         await msg.delete()
         await asyncio.sleep(3.5)
         await gif.delete()
         for j in range(4):
            judge = []
            emoji=""
            gif, msg = await self.slot_maker(ctx, ["picture/bonus/yattemiyo.gif"], "kamiyanao_slot", 5)
            for i in range(5):
               if i<3:
                  ran = ei[i]
               elif j == 3 and i==3:
                  ran = ei[i]
               else:
                  ran = random.choice(ei)
               judge.append(ran)
               emoji += str(self.bot.get_emoji(ran))
               if j == 3:
                  await msg.edit(content=emoji)
                  await asyncio.sleep(0.3)
            if j == 3:
               await asyncio.sleep(1)
               await gif.delete()
               if ei==judge:
                  return msg
               else:
                  return False

            await msg.edit(content=emoji)
            await asyncio.sleep(1)
            if ei == judge:
               return msg
            await gif.delete()
            await msg.delete()
      else:
         return False


   async def slot_maker(self, ctx, num,slot,count):
      emoji=""
      for i in range(count):
         emoji += str(self.bot.get_emoji(int(os.environ.get(slot))))
      if num==1:
         msg=await ctx.send(emoji)
         return msg
      else:
         gif=await ctx.send(file=discord.File(random.choice(num)))
         msg=await ctx.send(emoji)
         await asyncio.sleep(3)
         return gif, msg
   
   async def slot_flag(self, ctx,slot):
      if ctx.channel.id != int(os.environ.get("naosuki_ch")):
         return False
      if self.slot == True:
         return False
      self.slot = True
      with (sqlite3.connect("db/bot_data.db")) as conn:
         c = conn.cursor()
         c.execute(f'select naosuki,mayuge_coin from userdata where id={ctx.author.id}')
         flag_list = c.fetchone()
         
      if slot=="naosuki":
         if flag_list[0]==1:
            await ctx.send(f"{ctx.author.mention}なおすきスロット,スーパーなおすきスロットは1日一回までだよ！")
            return False
         else:
            c.execute(f'update userdata set naosuki=1 where id={ctx.author.id}')
            conn.commit()
      elif slot == "24_hours":
         if flag_list[1] == 0:
            await ctx.send(f"{ctx.author.mention}まゆげコインが足りません")
            return False
         else:
            c.execute(f'update userdata set mayuge_coin=mayuge_coin-1 where id={ctx.author.id}')
            conn.commit()
            return flag_list[1]-1
      else:
         if flag_list[1] <5:
            await ctx.send(f"{ctx.author.mention}連続チャレンジは5つコインが必要です")
            return False
         else:
            c.execute(f'update userdata set mayuge_coin=mayuge_coin-5 where id={ctx.author.id}')
            conn.commit()

            return flag_list[1] - 5
         

      return True
   
      
   @commands.command("なおすきスロット")
   async def naosuki_slot(self, ctx):
      """スロットで遊びます"""
     
      if await self.slot_flag(ctx, "naosuki") == False:
         self.slot = False
         return
         
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji=""
      judge=[]
      ei=emdic["naosuki"]
      path = "picture/gif/*.gif"
      num = glob.glob(path)
      gif,msg=await self.slot_maker(ctx,num,"naosuki_emoji",4)

      emoji = ""
      if random.randint(1, 200) == 70:
         sp_emoji=self.get_emoji()   
         for i in sp_emoji:
            if i == "\n":
               emoji += "\n"
               await msg.edit(content=emoji)
               await asyncio.sleep(0.4)
            elif i == 0:
               await msg.edit(content=emoji)
               await asyncio.sleep(0.4)
            else:
               emoji += str(self.bot.get_emoji(i))
         await msg.edit(content=emoji)
      else:
         for i in range(4):
            ran=random.choice(ei)
            judge.append(ran)
            emoji += str(self.bot.get_emoji(ran))
            await asyncio.sleep(0.3)
            await msg.edit(content=emoji)
         
         if ei == judge:
            emoji = emdic["nao_gif"]
            for i in emoji:
               ej = str(self.bot.get_emoji(i))
               await msg.add_reaction(ej)
            await ctx.send(f"{ctx.author.mention}なおすき！なおすき！なおすき！")
      await gif.delete()
      self.slot = False
   
   @commands.command("スーパーなおすきスロット")
   async def super_naosuki_slot(self, ctx):
      """スロットで遊びます"""
     
      if await self.slot_flag(ctx, "naosuki") == False:
         self.slot = False
         return
         
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji=""
      judge=[]
      ei=emdic["naosuki_english"]

      for i in emdic["rainbow_art"]:
          emoji += str(self.bot.get_emoji(int(i)))
      rainbow1=await ctx.send(emoji)
      msg=await self.slot_maker(ctx,1,"naosuki_english",7)
      rainbow2=await ctx.send(emoji)
      await asyncio.sleep(3)
      emoji = ""
      if random.randint(1, 1000) == 70:
         sp_emoji=emdic["2ndSIDE"] 
         for i in sp_emoji:
            emoji += str(self.bot.get_emoji(i))
         await msg.edit(content=emoji)
      else:
         for i in range(7):
            ran=random.choice(ei)
            judge.append(ran)
            emoji += str(self.bot.get_emoji(ran))   
         await msg.edit(content=emoji)
         
         if ei == judge:
            emoji = emdic["nao_gif"]
            for i in emoji:
               ej = str(self.bot.get_emoji(i))
               await msg.add_reaction(ej)
            await ctx.send(f"{ctx.author.mention}なおすき！なおすき！なおすき！")
      await rainbow1.delete()
      await rainbow2.delete()
      self.slot = False
   
   @commands.command("レインボースロット")
   async def side(self, ctx):
      """スロットで遊びます"""
     
      coin=await self.slot_flag(ctx, "24_hours")
      if coin == False:
         self.slot = False
         return
      log=await ctx.send(f"{ctx.author.mention}残り{coin}まゆげコイン")
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji=""
      judge=[]
      ei=emdic["2ndSIDE"]

      for i in emdic["rainbow_art"]:
          emoji += str(self.bot.get_emoji(int(i)))
      rainbow1=await ctx.send(emoji)
      msg=await self.slot_maker(ctx,1,"2ndSIDE",7)
      rainbow2=await ctx.send(emoji)
      await asyncio.sleep(3)
      emoji = ""
      if random.randint(1, 1000) == 70:
         sp_emoji=emdic["2ndSIDE"] 
         for i in sp_emoji:
            emoji += str(self.bot.get_emoji(i))
         await msg.edit(content=emoji)
      else:
         for i in range(7):
            ran=random.choice(ei)
            judge.append(ran)
            emoji += str(self.bot.get_emoji(ran))   
         await msg.edit(content=emoji)
         
         if ei == judge:
            emoji = emdic["nao_gif"]
            for i in emoji:
               ej = str(self.bot.get_emoji(i))
               await msg.add_reaction(ej)
            await ctx.send(f"{ctx.author.mention}虹色橋が完成した")
      await rainbow1.delete()
      await rainbow2.delete()
      await log.delete()
      self.slot = False
   
   @commands.command("神谷奈緒チャレンジ")
   async def hours24_slot(self, ctx):
      """スロットで遊びます"""
      coin=await self.slot_flag(ctx, "24_hours")
      if coin == False:
         self.slot = False
         return
      log=await ctx.send(f"{ctx.author.mention}残り{coin}まゆげコイン")
      
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji=""
      judge=[]
      ei=emdic["kamiyanao"]
      path = "picture/gif2/*.gif"
      num = glob.glob(path)
      gif,msg=await self.slot_maker(ctx,num,"kamiyanao_slot",5)
      emoji = ""
      for i in range(5):
         ran=random.choice(ei)
         judge.append(ran)
         emoji += str(self.bot.get_emoji(ran))
         await asyncio.sleep(0.1)
         await msg.edit(content=emoji)
      answer = await self.bonus_slot(ctx, ei, judge, msg)
      if answer != False and answer!=True:
         msg=answer
      if ei == judge or answer!=False:
         emoji = emdic["nao_gif"]
         emoji+= emdic["kamiyanao"]
         emoji += emdic["naosuki"]
         for i in emoji:
            ej = str(self.bot.get_emoji(i))
            try:
               await msg.add_reaction(ej)
            except AttributeError:
               pass
         await ctx.send(f"{ctx.author.mention}チャレンジ成功！！")
      await gif.delete()
      await log.delete()
      self.slot = False
      

   @commands.command("連続神谷奈緒チャレンジ")
   async def con_hours24_slot(self, ctx):
      """スロットで遊びます"""
      coin=await self.slot_flag(ctx, "24_5hours")
      if coin == False:
         self.slot = False
         return
      log=await ctx.send(f"{ctx.author.mention}残り{coin}まゆげコイン")
      
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji=""
      judge=[]
      ei=emdic["kamiyanao"]
      path = "picture/gif2/*.gif"
      num = glob.glob(path)
      for j in range(5):
         for i in range(5):
            emoji += str(self.bot.get_emoji(751709132087754763))
         emoji+="\n"
      gif=await ctx.send(file=discord.File(random.choice(num)))
      msg=await ctx.send(emoji)
      await asyncio.sleep(1)

      emoji = ""
      moji = ""
      tmp=[]
      moji2=[[],[],[],[],[]]
      for j in range(5):
         judge.append(random.choice(ei) for i in range(5))
      for j in range(5):
         tmp.append([str(self.bot.get_emoji(i)) for i in judge[j]])

      ran = []
      for j in range(5):
         ran.append([x[j] for x in tmp])
      for i in ran:
         for j in range(5):
            moji2[j % 5].append(i[j])
         
         for i in range(5):
            moji += "".join(moji2[i]) + "\n"
         await msg.edit(content=moji)
         await asyncio.sleep(0.1)        
         moji=""
 
      for i in judge:
         if ei ==i :
            emoji = emdic["nao_gif"]
            emoji+= emdic["kamiyanao"]
            emoji += emdic["naosuki"]
            for i in emoji:
               ej = str(self.bot.get_emoji(i))
               await msg.add_reaction(ej)
            await ctx.send(f"{ctx.author.mention}チャレンジ成功！！")
            self.chance = True
            break
      for i in judge:
         if self.chance == False:
            answer = await self.bonus_slot(ctx, ei, judge, msg)
      await gif.delete()
      await log.delete()
      self.slot = False
      

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Game(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
