import os
import traceback
from os.path import dirname, join

import discord
from discord.ext import commands
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
INITIAL_EXTENSIONS = [
    'cog.bot_cog',
    "cog.music_cog",
    "cog.timeprocess_cog",
    "cog.game_cog",
    "cog.idol_cog",
    "cog.debug_cog",
    "cog.funny_cog",
    "cog.dispander",
    "cog.convenience_cog"
]


class NAO(commands.Bot):

   def __init__(self, command_prefix, intents):
      super().__init__(command_prefix, intents=intents)
      for cog in INITIAL_EXTENSIONS:
         try:
            self.load_extension(cog)
         except Exception:
            traceback.print_exc()

   async def on_ready(self):
      print('起動しました')
      print(self.user.name)
      

if __name__ == '__main__':
   intents = discord.Intents.all()
   bot = NAO(command_prefix='!', intents=intents)
   bot.run(os.environ.get("NAO"))  # トークン
