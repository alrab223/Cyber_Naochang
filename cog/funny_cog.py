import glob
import json
import os
import random

import discord
import requests
from discord.ext import commands
from discord_components import Button, ButtonStyle, DiscordComponents, Select, SelectOption
from PIL import Image

from cog.utils import picture_download as pd
from cog.utils import wiki_search
from cog.utils.DbModule import DbModule as db
from cog.utils.webhook_control import Webhook_Control


class Funny(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.db = db()
      DiscordComponents(self.bot)
      with open("json/picture.json", "r") as f:
         self.colla_num = json.load(f)

   @commands.command()
   async def gold(self, ctx):
      """所持まゆげを調べます"""
      gold = self.db.select(
          f'select gold from user_data where id={ctx.author.id}')
      await ctx.send(f"{gold[0]['gold']}まゆげ")

   @commands.command("教えて奈緒")
   async def wiki(self, ctx, word: str):
      """wikipediaを調べます。引数(単語)"""
      await ctx.send(wiki_search.wikipediaSearch(word))

   @commands.command()
   async def rainbow(self, ctx):
      await ctx.message.delete()
      webhook = await Webhook_Control.get_webhook(ctx)
      await webhook.send(content=":heart: :orange_heart: :yellow_heart: :green_heart: :blue_heart: :purple_heart:",
                         username=ctx.author.display_name,
                         avatar_url=ctx.author.avatar_url_as(format="png"))

   @commands.command()
   async def rainbow2(self, ctx):
      emoji = ""
      await ctx.message.delete()
      webhook = await Webhook_Control.get_webhook(ctx)
      with open("json/emoji.json", "r")as f:
         dic = json.load(f)
      for i in dic["rainbow_art"]:
         emoji += str(self.bot.get_emoji(int(i)))
      await webhook.send(content=emoji,
                         username=ctx.author.display_name,
                         avatar_url=ctx.author.avatar_url_as(format="png"))

   @commands.command()
   async def rainbow3(self, ctx):
      emoji = ""
      await ctx.message.delete()
      webhook = await Webhook_Control.get_webhook(ctx)
      with open("json/emoji.json", "r")as f:
         dic = json.load(f)
      text = dic["rainbow_art"]
      for i in range(7):
         for i in text:
            emoji += str(self.bot.get_emoji(int(i)))
         emoji += "\n"
         pop = text.pop(0)
         text.append(pop)
      await webhook.send(content=emoji,
                         username=ctx.author.display_name,
                         avatar_url=ctx.author.avatar_url_as(format="png"))
   
   def quickpick_process(self, ticket: str, starters: int):
      horse = range(1, starters + 1)
      if ticket == "単勝,複勝":
         vote = random.sample(horse, 1)
      elif ticket == "馬連":
         vote = random.sample(horse, 2)
         vote.sort()
      elif ticket == "馬単":
         vote = random.sample(horse, 2)
      elif ticket == "ワイド":
         vote = random.sample(horse, 2)
         vote.sort()
      elif ticket == "3連複":
         vote = random.sample(horse, 3)
         vote.sort()
      else:
         vote = random.sample(horse, 3)
      vote = [str(i) for i in vote]
      vote = "→".join(vote)
      return vote
   
   @ commands.command("クイックピック")
   async def quickpick(self, ctx, starters: int):
      comp = []
      comp2 = []
      ticket = ["単勝,複勝", "馬連", "馬単", "ワイド", "3連複", "3連単"]
      for i, name in enumerate(ticket):
         if i < 5:
            comp.append(Button(style=ButtonStyle.blue, label=name))
         else:
            comp2.append(Button(style=ButtonStyle.blue, label=name))

      await ctx.send(
          f"出走数は{starters}頭です。馬券の種類を選択してください",
          components=[
              comp,
              comp2,
          ],
      )
      while True:
         interaction = await self.bot.wait_for("button_click")
         print(interaction.user.display_name)
         vote = self.quickpick_process(interaction.component.label, starters)
         vote = f"{interaction.component.label}\n{vote}"
         await interaction.respond(content=vote, ephemeral=True)

   def paste(self, img_list):
      img_width = 0
      dst = Image.new('RGBA', (120 * len(img_list), 120))
      for img in img_list:

         img = img.resize((120, 120))
         dst.paste(img, (img_width, 0))
         img_width += img.width
      return dst

   def paste2(self, img_list):
      img_height = 0
      dst = Image.new('RGBA', (120, 120 * len(img_list)))
      for img in img_list:

         img = img.resize((120, 120))
         dst.paste(img, (0, img_height))
         img_height += img.height
      return dst

   @commands.command(aliases=["スタンプ", "b", "big"])
   async def stamp(self, ctx, *emoji: discord.Emoji):
      await ctx.message.delete()
      webhook = await Webhook_Control.get_webhook(ctx)

      if len(emoji) < 2:
         url = emoji[0].url
         await webhook.send(content=url,
                            username=ctx.author.display_name,
                            avatar_url=ctx.message.author.avatar_url_as(format="png"))
      else:
         for i, emoji in enumerate(emoji):
            pd.download_img(emoji.url, f"picture/emojis/emoji{i}.png")
         png_name = sorted(glob.glob('picture/emojis/*png'))
         im_list = []
         for file_name in png_name:
            Image_tmp = Image.open(file_name)
            im_list.append(Image_tmp)
         self.paste(im_list).save("picture/emojis/union_emoji.png")
         await webhook.send(file=discord.File("picture/emojis/union_emoji.png"),
                            username=ctx.author.display_name,
                            avatar_url=ctx.message.author.avatar_url_as(format="png"))
         for i in sorted(glob.glob('picture/emojis/*png')):
            os.remove(i)

   @commands.command("なおすきボタン")
   async def naosuki_button(self, ctx, ch_id=None):
      if ch_id is None:
         channel = ctx.channel
      else:
         channel = self.bot.get_channel(744610643927236750)
      await channel.send(
          "まゆげ",
          components=[
              [Button(style=ButtonStyle.blue, label="なおすき")],
          ],
      )
      while True:
         interaction = await self.bot.wait_for("button_click")
         # print(interaction.user.display_name)
         url = 'https://discord.com/'
         if interaction.component.label == "なおすき":
            self.db.update('update naosuki_count set count=count+1')
            await interaction.respond(content="なおすきカウントが増えた", ephemeral=True)

   @commands.command(aliases=["d"])
   async def stamp2(self, ctx, *emoji: discord.Emoji):
      await ctx.message.delete()
      webhook = await Webhook_Control.get_webhook(ctx)

      if len(emoji) < 2:
         url = emoji[0].url
         await webhook.send(content=url,
                            username=ctx.author.display_name,
                            avatar_url=ctx.message.author.avatar_url_as(format="png"))
      else:
         for i, emoji in enumerate(emoji):
            pd.download_img(emoji.url, f"picture/emojis/emoji{i}.png")
         png_name = sorted(glob.glob('picture/emojis/*png'))
         im_list = []
         for file_name in png_name:
            Image_tmp = Image.open(file_name)
            im_list.append(Image_tmp)
         self.paste2(im_list).save("picture/emojis/union_emoji.png")
         await webhook.send(file=discord.File("picture/emojis/union_emoji.png"),
                            username=ctx.author.display_name,
                            avatar_url=ctx.message.author.avatar_url_as(format="png"))
         for i in sorted(glob.glob('picture/emojis/*png')):
            os.remove(i)

   @commands.command(aliases=["u", "unicode"])
   async def normal_emoji(self, ctx, emojis: str):
      try:
         emojis = f"{ord(emojis):x}"
         url = f"https://bot.mods.nyc/twemoji/{emojis}.png"
      except TypeError:
         await ctx.reply("その絵文字は対応していません、ごめんね")
         return
      await ctx.message.delete()
      webhook = await Webhook_Control.get_webhook(ctx)
      await webhook.send(content=url,
                         username=ctx.author.display_name,
                         avatar_url=ctx.message.author.avatar_url_as(format="png"))

   @commands.Cog.listener()
   async def on_message(self, message):
      if message.author.bot:
         return
      if "なおはじ" in message.content:
         emoji = [
             "<:na:681866058055024801>",
             "<:o_:681866075935211555>",
             "<:ha:681866087402700829>",
             "<:ji:681866097858969677>"]
         for i in emoji:
            await message.add_reaction(i)
      if "ｶﾐﾔﾅｵ" in message.content:
         emoji = [
             "<a:kamiya:714088347924168714>",
             "<a:unnamed:714091501646381058>",
             "<a:Nao_Loading_5:714091475444432917>",
             "<a:nao:714091488899891200>",
             "<a:1478254807_tHGkQDRV:714091363360047205>",
             "<a:1478254807_4CbzcReG:714091384411389952>",
         ]
         for i in emoji:
            await message.add_reaction(i)
      if "なおすき" in message.content:
         self.db.update('update naosuki_count set count=count+1')


def setup(bot):
   bot.add_cog(Funny(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
