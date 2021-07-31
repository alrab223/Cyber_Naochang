'''
MIT License

Copyright (c) 2019 1ntegrale9

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from discord import Embed
from discord.ext import commands
import re

regex_discord_message_url = (
    'https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
)


class ExpandDiscordMessageUrl(commands.Cog):
   def __init__(self, bot):
      self.bot = bot

   @commands.Cog.listener()
   async def on_message(self, message):
      if message.author.bot:
         return
      await dispand(message)


async def dispand(message):
   messages = await extract_messsages(message)
   for m in messages:
      if message.content:
         await message.channel.send(embed=compose_embed(m))
      for embed in m.embeds:
         await message.channel.send(embed=embed)


async def extract_messsages(message):
   messages = []
   for ids in re.finditer(regex_discord_message_url, message.content):
      if message.guild.id != int(ids['guild']):
         return
      fetched_message = await fetch_message_from_id(
          guild=message.guild,
          channel_id=int(ids['channel']),
          message_id=int(ids['message']),
      )
      messages.append(fetched_message)
   return messages


async def fetch_message_from_id(guild, channel_id, message_id):
   channel = guild.get_channel(channel_id)
   message = await channel.fetch_message(message_id)
   return message


def compose_embed(message):
   embed = Embed(
       description=message.content,
       timestamp=message.created_at,
       title='引用元',
       url=message.jump_url
   )
   embed.set_author(
       name=message.author.display_name,
       icon_url=message.author.avatar_url,
   )
   embed.set_footer(
       text=message.channel.name,
       icon_url=message.guild.icon_url,
   )
   if message.attachments and message.attachments[0].proxy_url:
      embed.set_image(
          url=message.attachments[0].proxy_url
      )
   return embed


def setup(bot):
   bot.add_cog(ExpandDiscordMessageUrl(bot))
