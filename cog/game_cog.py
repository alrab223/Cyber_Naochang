import asyncio
import glob
import json
import os
import random

import discord
from discord.ext import commands
from discord_components import (Button, ButtonStyle, DiscordComponents, Select,
                                SelectOption)
from PIL import Image

from cog.utils import picture_download as pd
from cog.utils.DbModule import DbModule as db
from cog.utils.webhook_control import Webhook_Control


class Game(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.handbattle = False
      self.slot = False
      self.chance = False
      self.db = db()
      DiscordComponents(self.bot)

   def get_emoji(self):
      with open("json/emoji.json", "r")as f:
         emoji = json.load(f)
      return emoji["special"][random.choice(list(emoji["special"].keys()))]

   @commands.command("")
   async def emoji(self, ctx):
      emoji = await ctx.guild.fetch_emojis()
      for i in emoji:
         print(i)

   async def bonus_slot(self, ctx, ei, judge, msg, slot_title, slot_num, debug=False, etc=False):
      count = 0
      for i, element in enumerate(ei):
         if judge[i] == element:
            count += 1

      if ((count == slot_num - 2 or count == slot_num - 1) and
              random.randint(1, slot_num) == 1) or debug:
         self.chance = True
         gif = await ctx.send("チャンス発生！！", file=discord.File("picture/bonus/triad.gif"))

         await msg.delete()
         await asyncio.sleep(3.5)
         await gif.delete()
         gif = await ctx.send(file=discord.File("picture/bonus/yattemiyo.gif"))
         for j in range(4):
            judge = []
            emoji = ""
            _, msg = await self.slot_maker(ctx, ['picture/bonus/yattemiyo.gif'], slot_title, slot_num, True)
            for i in range(slot_num):
               if i < slot_num - 2:
                  ran = ei[i]
               elif j == 3 and i == slot_num - 2:
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
               if ei == judge:
                  return msg
               else:
                  return False

            await msg.edit(content=emoji)
            await asyncio.sleep(1)
            if ei == judge:
               return msg
            if j == 3:
               await gif.delete()
            await msg.delete()
      else:
         return False

   async def slot_maker(self, ctx, num, slot, count, bonus=False):
      emoji = ""
      for i in range(count):
         emoji += str(self.bot.get_emoji(int(os.environ.get(slot))))
      if num == 1:
         msg = await ctx.send(emoji)
         return msg
      else:
         if bonus:
            gif = False
         else:
            gif = await ctx.send(file=discord.File(random.choice(num)))
         msg = await ctx.send(emoji)
         await asyncio.sleep(3)
         return gif, msg

   async def slot_flag(self, ctx, debug):
      # if ctx.channel.id != int(os.environ.get("naosuki_ch")) and debug is False:
      #    return False
      if self.slot is True:
         return False
      self.slot = True

   async def naosuki_slot_setup(self, ctx, debug=False):
      if await self.slot_flag(ctx, debug) is False:
         return False

      flag_list = self.db.select(f'select naosuki from user_data where id={ctx.author.id}')[0]

      if flag_list['naosuki'] == 1:
         await ctx.reply("なおすきスロット,スーパーなおすきスロットは1日一回までだよ！")
         return False
      else:
         self.db.update(f'update user_data set naosuki=1 where id={ctx.author.id}')

   async def slot_setup(self, ctx, slot: str, debug=False):
      if await self.slot_flag(ctx, debug) is False:
         return False

      with open('json/slot_data.json', 'r')as f:  # スロットの種類と使用コイン数を取得
         slot_data = json.load(f)

      flag_list = self.db.select(f'select mayuge_coin from user_data where id={ctx.author.id}')[0]
      if flag_list['mayuge_coin'] >= slot_data[slot]:
         self.db.update(f'update user_data set mayuge_coin=mayuge_coin-{slot_data[slot]} where id={ctx.author.id}')
         return flag_list['mayuge_coin'] - slot_data[slot]
      else:
         await ctx.reply(f"まゆげコインが足りません。コインが{slot_data[slot]}枚必要です")
         return False

   async def naosuki_special(self, msg):
      reel = ''
      sp_emoji = self.get_emoji()
      for i in sp_emoji:
         if i == "\n":
            reel += "\n"
            await msg.edit(content=reel)
            await asyncio.sleep(0.4)
         elif i == 0:
            await msg.edit(content=reel)
            await asyncio.sleep(0.4)
         else:
            reel += str(self.bot.get_emoji(i))
      await msg.edit(content=reel)

   @commands.command("なおすきスロット")
   async def naosuki_slot(self, ctx, debug=False, special_slot=False):
      """スロットで遊びます"""

      if await self.naosuki_slot_setup(ctx, debug) is False:
         self.slot = False
         return
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      target = emdic["naosuki"]  # 当たりリールを保存する変数
      path = "picture/gif/*.gif"
      num = glob.glob(path)
      gif, msg = await self.slot_maker(ctx, num, "naosuki_emoji", 4)
      if random.randint(1, 200) == 70 or special_slot is True:
         await self.naosuki_special(msg)
      else:
         judge = []  # 全リールを保存するリスト
         reel: str = ''  # リールを保存する変数
         for i in range(4):
            ran = random.choice(target)
            judge.append(ran)
            reel += str(self.bot.get_emoji(ran))
            await asyncio.sleep(0.3)
            await msg.edit(content=reel)

         if target == judge:
            reel = emdic["nao_gif"]
            for i in reel:
               ej = str(self.bot.get_emoji(i))
               await msg.add_reaction(ej)
            await ctx.send(f"{ctx.author.mention}なおすき！なおすき！なおすき！")
      await gif.delete()
      self.slot = False

   @commands.command("スーパーなおすきスロット")
   async def super_naosuki_slot(self, ctx, debug=False):
      """スロットで遊びます"""

      # if await self.naosuki_slot_setup(ctx, debug) is False:
      #    self.slot = False
      #    return
      webhook_c = Webhook_Control()
      webhook = await webhook_c.get_webhook(ctx)
      webhook_url = webhook.url
      urls = []
      with open('json/gif_url.json', 'r')as f:
         gif_list = json.load(f)
      urls.append(random.choice(gif_list['KAMIYANAO_PETIT']))
      urls.append(gif_list['NAOSUKI_SLOT'])
      urls.append(gif_list['SUPER_NAOSUKI_SLOT'])
      urls.append(gif_list['RAINBOW_GIF'])
      webhook_c.image_add(urls)
      webhook_c.add_title(title='スーパーなおすきスロット')
      webhook_c.webhook_send(webhook_url)
      await asyncio.sleep(5)
      async for log in ctx.channel.history(limit=10):
         if log.author.id == webhook.id:
            await log.delete()
            break
      with open('json/emoji.json', 'r')as f:
         emoji_dic = json.load(f)
      judge = []
      reels = ''
      for i in range(4):
         reel = random.choice(emoji_dic['super_naosuki_slot'])
         judge.append(reel)
         reels += str(self.bot.get_emoji(reel))
         await asyncio.sleep(0.3)
         if i == 0:
            msg = await ctx.send(reels)
         else:
            await msg.edit(content=reels)

      if judge.count(judge[0]) == len(judge):
         reaction = emoji_dic["nao_gif"]
         for i in reaction:
            ej = str(self.bot.get_emoji(i))
            await msg.add_reaction(ej)
      self.slot = False

   @commands.command("レインボースロット")
   async def side(self, ctx, debug=False):
      """スロットで遊びます"""

      coin = await self.slot_setup(ctx, "RAINBOW_SLOT", debug)
      if not coin:
         self.slot = False
         return
      log = await ctx.send(f"{ctx.author.mention}残り{coin}まゆげコイン")
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji = ""
      judge = []
      ei = emdic["2ndSIDE"]

      for i in emdic["rainbow_art"]:
         emoji += str(self.bot.get_emoji(int(i)))
      rainbow1 = await ctx.send(emoji)
      msg = await self.slot_maker(ctx, 1, "2ndSIDE", 7)
      rainbow2 = await ctx.send(emoji)
      await asyncio.sleep(3)
      emoji = ""
      if random.randint(1, 1000) == 70:
         sp_emoji = emdic["2ndSIDE"]
         for i in sp_emoji:
            emoji += str(self.bot.get_emoji(i))
         await msg.edit(content=emoji)
      else:
         for i in range(7):
            ran = random.choice(ei)
            judge.append(ran)
            emoji += str(self.bot.get_emoji(ran))
         await msg.edit(content=emoji)
         answer = await self.bonus_slot(ctx, ei, judge, msg, '2ndSIDE', 7, debug)
         if ei == judge or answer:
            msg = answer
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
   async def hours24_slot(self, ctx, debug=False):
      """スロットで遊びます"""
      coin = await self.slot_setup(ctx, "NAO_CHALLENGE", debug)
      if not coin:
         self.slot = False
         return
      log = await ctx.send(f"{ctx.author.mention}残り{coin}まゆげコイン")

      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji = ""
      judge = []
      ei = emdic["kamiyanao"]
      path = "picture/gif2/*.gif"
      num = glob.glob(path)
      gif, msg = await self.slot_maker(ctx, num, "kamiyanao_slot", 5)
      emoji = ""
      for i in range(5):
         ran = random.choice(ei)
         judge.append(ran)
         emoji += str(self.bot.get_emoji(ran))
         await asyncio.sleep(0.1)
         await msg.edit(content=emoji)
      answer = await self.bonus_slot(ctx, ei, judge, msg, "kamiyanao_slot", 5, debug)
      if answer and answer is True:
         msg = answer
      if ei == judge or answer:
         emoji = emdic["nao_gif"]
         emoji += emdic["kamiyanao"]
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

   async def nao_slot(self, ctx, debug=False, interaction=None):
      """スロットで遊びます"""
      coin = await self.slot_setup(ctx, "NAO_CHALLENGE", debug)
      if not coin:
         self.slot = False
         return
      log = await ctx.send(f"{interaction.author.mention}残り{coin}まゆげコイン")

      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji = ""
      judge = []
      ei = emdic["kamiyanao"]
      path = "picture/gif2/*.gif"
      num = glob.glob(path)
      gif, msg = await self.slot_maker(ctx, num, "kamiyanao_slot", 5)
      emoji = ""
      for i in range(5):
         ran = random.choice(ei)
         judge.append(ran)
         emoji += str(self.bot.get_emoji(ran))
         await asyncio.sleep(0.1)
         await msg.edit(content=emoji)
      answer = await self.bonus_slot(ctx, ei, judge, msg, "kamiyanao_slot", 5, debug)
      if answer and answer is True:
         msg = answer
      if ei == judge or answer:
         emoji = emdic["nao_gif"]
         emoji += emdic["kamiyanao"]
         emoji += emdic["naosuki"]
         for i in emoji:
            ej = str(self.bot.get_emoji(i))
            try:
               await msg.add_reaction(ej)
            except AttributeError:
               pass
         await ctx.send(f"{interaction.author.mention}チャレンジ成功！！")
      await gif.delete()
      await log.delete()
      self.slot = False

   def paste(self, img_list):
      img_width = 0
      dst = Image.new('RGBA', (120 * len(img_list), 120))
      for img in img_list:

         img = img.resize((120, 120))
         dst.paste(img, (img_width, 0))
         img_width += img.width
      return dst

   async def chiba_slot(self, channel, debug=False, interaction=None):
      """スロットで遊びます"""
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji = ""
      judge = []
      ei = emdic["makuhari"]
      path = "picture/gif/chiba.gif"
      emoji = ""
      for i in range(4):
         emoji += str(self.bot.get_emoji(913838697730940978))
      msg = await channel.send(emoji)
      gif = await channel.send(file=discord.File(path))
      await asyncio.sleep(3)
      emoji = ""
      for i in range(4):
         ran = random.choice(ei)
         judge.append(ran)
         emoji += str(self.bot.get_emoji(ran))
         await asyncio.sleep(0.1)
         await msg.edit(content=emoji)
      if debug is True:
         ei = judge
      if ei == judge:
         emoji = emdic["nao_gif"]
         emoji += emdic["kamiyanao"]
         emoji += emdic["naosuki"]
         for i in emoji:
            ej = str(self.bot.get_emoji(i))
            try:
               await msg.add_reaction(ej)
            except AttributeError:
               pass
         await channel.send(f"{interaction.author.mention}まくはり～")
      await gif.delete()
      self.slot = False
   
   async def chiba_slot2(self, channel, debug=False, interaction=None):
      """スロットで遊びます"""
      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji = ""
      judge = []
      ei = emdic["makuhari"]
      path = "picture/gif/chiba.gif"
      emoji = ""
      for i in range(4):
         emoji += str(self.bot.get_emoji(913838697730940978))
      msg = await channel.send(emoji)
      gif = await channel.send(file=discord.File(path))
      await asyncio.sleep(3)
      emoji = ""
      for i in range(4):
         ran = random.choice(ei)
         judge.append(ran)
      for i, emoji in enumerate(judge):
         emo = self.bot.get_emoji(emoji)
         print(emo.url)
         pd.download_img(emo.url, f"picture/emojis/emoji{i}.png")
      png_name = sorted(glob.glob('picture/emojis/*png'))
      im_list = []
      for file_name in png_name:
         Image_tmp = Image.open(file_name)
         im_list.append(Image_tmp)
      self.paste(im_list).save("picture/emojis/union_emoji.png")
      await channel.send(file=discord.File("picture/emojis/union_emoji.png"))
      for i in sorted(glob.glob('picture/emojis/*png')):
         os.remove(i)
      await msg.delete()
      if debug is True:
         ei = judge
      if ei == judge:
         emoji = emdic["nao_gif"]
         emoji += emdic["kamiyanao"]
         emoji += emdic["naosuki"]
         for i in emoji:
            ej = str(self.bot.get_emoji(i))
            try:
               await msg.add_reaction(ej)
            except AttributeError:
               pass
         await channel.send(f"{interaction.author.mention}まくはり～")
      await gif.delete()
      self.slot = False

   @commands.command("スロットボタン")
   async def slot_button(self, ctx, ch_id: int = None):
      if ch_id is None:
         channel = ctx.channel
      else:
         channel = self.bot.get_channel(ch_id)
      await channel.send(
          "幕張は出るか",
          components=[
              [Button(style=ButtonStyle.blue, label="ちば")],
          ],
      )
      await ctx.message.delete()
      while True:
         interaction = await self.bot.wait_for("button_click")
         if interaction.component.label == "ちば":
            msg = await interaction.respond(content="まくはり～", ephemeral=True)
            await self.nao_slot(ctx, False, interaction)
            await msg.delete()

   @commands.command("ちばボタン")
   async def chiba_button(self, ctx, ch_id: int = None):
      if ch_id is None:
         channel = ctx.channel
      else:
         channel = self.bot.get_channel(ch_id)
      await channel.send(
          "幕張は出るか。ボタンが見えなくなったら「!ちばボタン」で呼び出し",
          components=[
              [Button(style=ButtonStyle.green, label="ちば")],
          ],
      )
      await ctx.message.delete()
      while True:
         interaction = await self.bot.wait_for("button_click")
         if interaction.component.label == "ちば":
            await interaction.respond(content=f"{interaction.author.display_name}が押しました。まくはりチャレンジ", ephemeral=False)
            await self.chiba_slot2(channel, False, interaction)
   
   @commands.command("連続神谷奈緒チャレンジ")
   async def con_hours24_slot(self, ctx):
      """スロットで遊びます"""
      coin = await self.slot_setup(ctx, "NAO_CHALLENGE5")
      if not coin:
         self.slot = False
         return
      log = await ctx.send(f"{ctx.author.mention}残り{coin}まゆげコイン")

      with open("json/emoji.json", "r") as f:
         emdic = json.load(f)
      emoji = ""
      judge = []
      ei = emdic["kamiyanao"]
      path = "picture/gif2/*.gif"
      num = glob.glob(path)
      for j in range(5):
         for i in range(5):
            emoji += str(self.bot.get_emoji(751709132087754763))
         emoji += "\n"
      gif = await ctx.send(file=discord.File(random.choice(num)))
      msg = await ctx.send(emoji)
      await asyncio.sleep(1)

      emoji = ""
      moji = ""
      tmp = []
      moji2 = [[], [], [], [], []]
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
         moji = ""

      for i in judge:
         if ei == i:
            emoji = emdic["nao_gif"]
            emoji += emdic["kamiyanao"]
            emoji += emdic["naosuki"]
            for i in emoji:
               ej = str(self.bot.get_emoji(i))
               await msg.add_reaction(ej)
            await ctx.send(f"{ctx.author.mention}チャレンジ成功！！")
            self.chance = True
            break

      await gif.delete()
      await log.delete()
      self.slot = False


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
   bot.add_cog(Game(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
