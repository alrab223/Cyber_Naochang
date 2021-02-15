import asyncio
import glob
import json
import os
import random
import sqlite3

import discord
from discord.ext import commands  # Bot Commands Frameworkのインポート
from gtts import gTTS


class MusicBot():

   def playlist_print(self, dic, id):
      count = 1
      queue_list = ""
      for name in dic[str(id)]["playlist"]:
         queue_list += f"{count}, {name}" + "\n" + "\n"
         count += 1
      return queue_list


# コグとして用いるクラスを定義。
class Music(commands.Cog, MusicBot):

   def __init__(self, bot):
      self.bot = bot
      self.volume = 0.1
      self.voich = None
      self.music_queue = []
      self.read = False
      self.read_count = 0

   @commands.command("カモン")
   async def voice_connect(self, ctx):
      """botをボイチャに召喚します"""

      self.voich = await discord.VoiceChannel.connect(ctx.author.voice.channel)

      self.voich.play(discord.FFmpegPCMAudio('music/nao_aisatsu.m4a'))
      self.voich.source = discord.PCMVolumeTransformer(self.voich.source)
      self.voich.source.volume = self.volume
      await asyncio.sleep(2)

   @commands.command("グッバイ")
   async def voice_disconnect(self, ctx):
      """botをボイチャから退出させます"""
      if self.voich.is_playing():
         self.voich.stop()
      self.voich.play(discord.FFmpegPCMAudio("music/hayate_tanosikatta.m4a"))
      self.voich.source = discord.PCMVolumeTransformer(self.voich.source)
      self.voich.source.volume = self.volume
      await asyncio.sleep(3)
      await self.voich.disconnect()
      self.voich = None

   @commands.command()
   async def se(self, ctx, se: str):
      """seを鳴らします(se)"""
      if self.voich.is_playing():
         self.voich.stop()
      if os.path.exists("music/" + se + ".mp3"):
         self.voich.play(discord.FFmpegPCMAudio(f'music/{se}.mp3'))
      else:
         self.voich.play(discord.FFmpegPCMAudio(f'music/{se}.m4a'))
      self.voich.source = discord.PCMVolumeTransformer(self.voich.source)
      self.voich.source.volume = self.volume

   @commands.command("pm")
   async def playlist_make(self, ctx, se: str):
      """プレイリストを作ります(se)"""
      if os.path.exists(
          "music/" +
          se +
          ".mp3") != True and os.path.exists(
          "music/" +
          se +
              ".m4a") != True:
         await ctx.send("SEが存在しません")
         return
      with open("json/bot_id.json", "r")as f:
         dic = json.load(f)
      dic[str(ctx.author.id)]["playlist"].append(se)
      queue_list = self.playlist_print(dic, ctx.author.id)
      embed = discord.Embed(title="あなたのプレイリスト", description=queue_list)
      embed.set_footer(text="この順番に再生されます")
      await ctx.send(embed=embed)
      with open("json/bot_id.json", "w")as f:
         json.dump(dic, f, indent=3)

   @commands.command("pd")
   async def playlist_delete(self, ctx):
      """プレイリストを消去します"""
      with open("json/bot_id.json", "r")as f:
         dic = json.load(f)
         dic[str(ctx.author.id)]["playlist"] = []
      with open("json/bot_id.json", "w")as f:
         json.dump(dic, f, indent=3)

   @commands.command("pc")
   async def playlist_check(self, ctx):
      """プレイリストを確認します"""
      with open("json/bot_id.json", "r")as f:
         dic = json.load(f)
      queue_list = self.playlist_print(dic, ctx.author.id)
      embed = discord.Embed(title="あなたのプレイリスト", description=queue_list)
      embed.set_footer(text="この順番に再生されます")
      await ctx.send(embed=embed)

   @commands.command("ps")
   async def playlist_set(self, ctx):
      """プレイリストをセットします"""
      with open("json/bot_id.json", "r")as f:
         dic = json.load(f)
      self.music_queue = dic[str(ctx.author.id)]["playlist"]
      queue_list = self.playlist_print(dic, ctx.author.id)
      embed = discord.Embed(title="あなたのプレイリスト", description=queue_list)
      embed.set_footer(text="この順番に再生されます")
      await ctx.send(embed=embed)
      await ctx.send("プレイリストをセットしました")

   @commands.command("q")
   async def queue(self, ctx, se: str):
      """キューをセットします(se)"""
      if os.path.exists("music/" + se + ".mp3") != True and os.path.exists("music/" + se + ".m4a") != True:
         await ctx.send("SEが存在しません")
         return
      self.music_queue.append(se)
      count = 1
      queue_list = ""
      for name in self.music_queue:
         queue_list += f"{count}, {name}" + "\n" + "\n"
         count += 1
      embed = discord.Embed(title="再生リスト", description=queue_list)
      embed.set_footer(text="この順番に再生されます")
      await ctx.send(embed=embed)

   @commands.command()
   async def play(self, ctx):
      """セットしたプレイリストを再生します"""
      if self.voich.is_playing():
         self.voich.stop()

      def check_error(er):
         try:
            se = self.music_queue.pop(0)
            if os.path.exists("music/" + se + ".mp3"):
               self.voich.play(
                   discord.FFmpegPCMAudio(f'music/{se}.mp3'),
                   after=check_error)
            else:
               self.voich.play(
                   discord.FFmpegPCMAudio(f'music/{se}.m4a'),
                   after=check_error)
            self.voich.source = discord.PCMVolumeTransformer(self.voich.source)
            self.voich.source.volume = self.volume
         except IndexError:
            return
      check_error(None)

   @commands.command()
   async def skip(self, ctx):
      """スキップ"""
      if self.voich.is_playing():
         self.voich.stop()

   @commands.command()
   async def pause(self, ctx):
      """ポーズ"""
      if self.voich.is_playing():
         self.voich.pause()

   @commands.command()
   async def stop(self, ctx):
      """停止"""
      if self.voich.is_playing():
         self.voich.stop()
         self.music_queue = []

   @commands.command()
   async def restart(self, ctx):
      """再開"""
      if self.voich.is_playing():
         pass
      else:
         self.voich.resume()

   @commands.command("読み上げ")
   async def read(self, ctx):
      if self.read:
         await ctx.send("読み上げをオフにしました")
      else:
         self.read = True
         await ctx.send("読み上げをオンにしました")

   @commands.Cog.listener()
   async def on_message(self, message):
      if message.content.startswith("<") == False and message.content.startswith("!") == False and message.content.startswith("http") == False and self.read == True:
         tts = gTTS(text=message.content, lang='ja')
         tts.save(f'music/mp3/tts{self.read_count}.mp3')
         self.read_count += 1
         if self.voich.is_playing():
            return
         num = glob.glob("music/mp3/*.mp3")

         def check_error(f):
            num = glob.glob("music/mp3/*.mp3")
            if len(num) > 0:
               os.remove(sorted(num)[0])
               self.voich.play(
                   discord.FFmpegPCMAudio(
                       sorted(num)[0]),
                   after=check_error)
               self.voich.source = discord.PCMVolumeTransformer(
                   self.voich.source)
               self.voich.source.volume = self.volume
               num = glob.glob("music/mp3/*.mp3")
            else:
               return

         self.voich.play(
             discord.FFmpegPCMAudio(
                 sorted(num)[0]),
             after=check_error)
         self.voich.source = discord.PCMVolumeTransformer(self.voich.source)
         self.voich.source.volume = self.volume

   @commands.Cog.listener()
   async def on_voice_state_update(self, member, before, after):
      if member.bot:
         return

      with (sqlite3.connect("db/bot_data.db")) as conn:
         c = conn.cursor()
         if after.channel is None and len(before.channel.members) == 1:
            c.execute('update vc_notification_setting set reset=0')
         try:
            sql = c.execute(
                'select id,members,reset,vc_notification from vc_notification_setting where vc_notification=1')
            id_list = [x for x in sql]
            for i in id_list:
               if len(
                       after.channel.members) >= i[1] and i[3] == 1 and i[2] == 0:
                  dm_channel = self.bot.get_user(i[0])
                  await dm_channel.send(f"{after.channel.name}に{len(after.channel.members)}以上います")
                  c.execute(
                      f'update vc_notification_setting set reset=1 where id={i[0]}')
         except AttributeError:
            pass
         conn.commit()

      if before.channel is None and self.voich is not None:
         if random.randint(1, 10) < 4:
            with open("text/voice_se.txt", "r") as f:
               text = f.readlines()
            await asyncio.sleep(0.7)
            self.voich.play(
                discord.FFmpegPCMAudio(random.choice(text).replace("\n", "")))
            self.voich.source = discord.PCMVolumeTransformer(self.voich.source)
            self.voich.source.volume = self.volume
         else:
            self.voich.play(discord.FFmpegPCMAudio('music/tissue_man.m4a'))

# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):

   bot.add_cog(Music(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
