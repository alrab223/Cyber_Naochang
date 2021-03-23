import json
import os
import subprocess

import discord
import requests
from discord.ext import commands
from cog.utils import colla
from cog.utils import picture_download as pd
from cog.utils.DbModule import DbModule as db


class Main(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.db = db()
      with open("json/picture.json", "r") as f:
         self.colla_num = json.load(f)

   @commands.is_owner()
   @commands.command("goodbye")
   async def disconnect(self, ctx):
      """botを切ります"""
      await ctx.send("また会いましょう")
      await self.bot.logout()

   @commands.command()
   async def ping(self, ctx):
      await ctx.send(f'応答速度:{round(self.bot.latency * 1000)}ms')

   @commands.Cog.listener()
   async def on_member_join(self, member):
      dm_channel = await member.create_dm()
      with open("text/introduce.txt", "r")as f:
         text = f.read()
      await dm_channel.send(member.mention)
      await dm_channel.send(text)
      self.db.insert("user_data", ["id", "gold", "birthday,naosuki", "vc_notification", "mayuge_coin"], [member.id, 10000, None, 0, 0, 10])

   @commands.command()
   async def server_status(self, ctx):
      text = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE, text=True).stdout.strip().split("=")
      text2 = subprocess.run(['free', '-m'], stdout=subprocess.PIPE, text=True).stdout.strip().split("=")
      text2 = text2[0].split(':')[1].split(' ')
      text2 = [x for x in text2 if x != '']
      embed = discord.Embed(title="サーバー状態")
      embed.add_field(name="CPU温度", value=f"{text[1]}")
      embed.add_field(name="メモリ使用量", value=f"{text2[1]}/{text2[0]}M")
      await ctx.send(embed=embed)

   @commands.Cog.listener()
   async def on_message(self, message):
      if message.author.bot:
         return
      if message.attachments:
         if message.content in self.colla_num:
            pd.download_img(
                message.attachments[0].url,
                "picture/colla/image.png")
            colla.colla_maker(self.colla_num[message.content])
            await message.delete()
            await message.channel.send(file=discord.File("picture/colla/new.png"))

         elif message.content == "切り抜き":
            pd.download_img(
                message.attachments[0].url,
                "picture/colla/image.png")
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open('picture/colla/image.png', 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': os.environ.get("removebg_api")},
            )
            if response.status_code == requests.codes.ok:
               with open('picture/colla/no-bg.png', 'wb') as out:
                  out.write(response.content)
            else:
               print("Error:", response.status_code, response.text)
            await message.delete()
            await message.channel.send(file=discord.File("picture/colla/no-bg.png"))


def setup(bot):
   bot.add_cog(Main(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
