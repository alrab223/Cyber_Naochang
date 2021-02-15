import asyncio
import json
import os
import re

from discord.ext import commands
from cog.utils.DbModule import DbModule as db


class Main(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.db = db()
      with open("json/picture.json", "r") as f:
         self.colla_num = json.load(f)

   @commands.is_owner()
   @commands.command("ナオビーム")
   async def logs(self, ctx, num: int):
      logs = []
      async for log in ctx.channel.history(limit=num):
         logs.append(log)
      await ctx.channel.delete_messages(logs)

   @commands.command("vc通知")
   @commands.dm_only()
   async def vc_news(self, ctx, num: str):
      if num == "オフ":
         self.db.update(
             f'update vc_notification set vc_notification=0 where id={ctx.author.id}')
         await ctx.send(ctx.author.mention + "通知を解除しました")
      else:
         self.db.update(
             f'update vc_notification set members={num},vc_notification=1 where id={ctx.author.id}')
         await ctx.send(f"参加人数{num}以上で通知します")

   @commands.dm_only()
   @commands.command("予約投稿")
   async def future_send(self, ctx, time: str, channel_id: int):
      def user_check(message):
         return message.author.id == ctx.author.id
      await ctx.send("メッセージを入力してください")
      msg = await self.bot.wait_for('message', check=user_check)

      await ctx.send("この内容でいいですか？間違い無ければ「はい」と入力してください")

      def user_check2(message):
         return message.author.id == ctx.author.id and message.content == "はい"
      try:
         await self.bot.wait_for('message', check=user_check2)
      except asyncio.TimeoutError:
         return
      self.db.allinsert("future_send", [ctx.author.id, msg.content, time, channel_id])

   @commands.Cog.listener()
   async def on_message(self, message):
      if message.author.bot:
         return
      pattern = "https?://[\\w/:%#\\$&\\?\\(\\)~\\.=\\+\\-]+"
      text: list = re.findall(pattern, message.content)
      ch_list: list = ["kami_ch", "ya_ch", "na_ch", "o_ch"]
      channels: list = []
      for i in ch_list:
         channels.append(self.bot.get_channel(int(os.environ.get(i))))
      if message.channel.id == channels[0].id or message.channel.id == channels[1].id or \
         message.channel.id == channels[2].id or message.channel.id == channels[3].id:

         for channel in channels:
            async for log in channel.history(limit=40):
               url_list: list = re.findall(pattern, log.content)
               if set(text) & set(url_list) and message.id != log.id:
                  msg = await message.channel.send(f"{message.author.mention}{channel.name}に同じURLがもう貼られてるよ！")
                  await asyncio.sleep(10)
                  await msg.delete()
                  return


def setup(bot):
   bot.add_cog(Main(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
