import asyncio
import csv
import glob
import json
import random

import discord
import requests
from discord.ext import commands
from libneko import EmbedNavigator
from cog.utils.DbModule import DbModule as db
from cog.utils.webhook_control import Webhook_Control


class Idol(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.db = db()

   @commands.command("ユニット検索")
   async def unit_search(self, ctx, *args):
      flag = 0
      count = 0
      embed1 = discord.Embed(description='ユニット名一覧 1')
      embed2 = discord.Embed(description='ユニット名一覧 2')
      embed3 = discord.Embed(description='ユニット名一覧 3')
      embed4 = discord.Embed(description='ユニット名一覧 4')
      pages = [embed1, embed2, embed3, embed4]
      pages2 = []
      pagesj = [False, False, False, False]
      with open("json/unit_kai.json", "r", encoding="utf_8_sig") as f:
         dic = json.load(f)
      for i in dic["results"]["bindings"]:
         for j in list(args):
            if j in i["メンバー"]["value"]:
               flag += 1
            else:
               break
            if flag == len(list(args)):
               if count < 6:
                  embed1.add_field(
                      name=i["ユニット名"]["value"],
                      value=i["メンバー"]["value"],
                      inline=False)
                  pagesj[0] = True
               elif count < 12:
                  pagesj[1] = True
                  embed2.add_field(
                      name=i["ユニット名"]["value"],
                      value=i["メンバー"]["value"],
                      inline=False)
               elif count < 18:
                  pagesj[2] = True
                  embed3.add_field(
                      name=i["ユニット名"]["value"],
                      value=i["メンバー"]["value"],
                      inline=False)
               else:
                  pagesj[3] = True
                  embed4.add_field(
                      name=i["ユニット名"]["value"],
                      value=i["メンバー"]["value"],
                      inline=False)
               count += 1
         flag = 0
      for i in range(4):
         if pagesj[i]:
            pages2.append(pages[i])
      nav = EmbedNavigator(ctx, pages2)
      nav.start()

   @commands.command("奈緒ルーレット")
   async def nao_roulette(self, ctx):
      webhook_c = Webhook_Control()
      webhook = await webhook_c.get_webhook(ctx)
      webhook_url = webhook.url
      urls = ['https://cdn.discordapp.com/attachments/658856327019495475/823585001908076614/nao.gif'] * 2
      webhook_c.image_add(urls)
      webhook_c.add_title(title='奈緒ルーレット')
      webhook_c.webhook_send(webhook_url)
      await asyncio.sleep(3)
      async for log in ctx.channel.history(limit=10):
         if log.author.id == webhook.id:
            await log.delete()
            break
      path = "picture/nao/*.jpg"
      num = glob.glob(path)
      await ctx.send(file=discord.File(random.choice(num)))

   @commands.command("肇ルーレット")
   async def hajime_roulette(self, ctx):
      webhook_c = Webhook_Control()
      webhook = await webhook_c.get_webhook(ctx)
      webhook_url = webhook.url
      urls = ['https://cdn.discordapp.com/attachments/658856327019495475/823582685485465600/hajime.gif'] * 2
      webhook_c.image_add(urls)
      webhook_c.add_title(title='肇ルーレット')
      webhook_c.webhook_send(webhook_url)
      await asyncio.sleep(3)
      async for log in ctx.channel.history(limit=10):
         if log.author.id == webhook.id:
            await log.delete()
            break
      path = "picture/hajime/*.jpg"
      num = glob.glob(path)
      await ctx.send(file=discord.File(random.choice(num)))

   @commands.command("なおはじルーレット")
   async def naohaji_roulette(self, ctx):
      with open('text/newcard.csv')as f:
         reader = [row for row in csv.reader(f)]
         nao_cards = [row for row in reader if '神谷奈緒' in row]
         hajime_cards = [row for row in reader if '藤原肇' in row]
         nao_card = random.choice(nao_cards)
         hajime_card = random.choice(hajime_cards)
      webhook_c = Webhook_Control()
      webhook = await webhook_c.get_webhook(ctx)
      urls = ['https://cdn.discordapp.com/attachments/658856327019495475/823585001908076614/nao.gif',
              'https://cdn.discordapp.com/attachments/658856327019495475/823582685485465600/hajime.gif']
      webhook_c.image_add(urls)
      webhook_c.add_title(title='なおはじルーレット')
      webhook_c.webhook_send(webhook.url)
      await asyncio.sleep(3)
      async for log in ctx.channel.history(limit=10):
         if log.author.id == webhook.id:
            await log.delete()
            break
      webhook_c = Webhook_Control()
      urls = [
          f'https://pink-check.school/image/withoutsign/{nao_card[1]}',
          f'https://pink-check.school/image/withoutsign/{hajime_card[1]}']
      webhook_c.image_add(urls)
      webhook_c.add_title(title='なおはじルーレット')
      webhook_c.add_field(name=nao_card[3].split(']')[0] + ']', value=nao_card[3].split(']')[1])
      webhook_c.add_field(name=hajime_card[3].split(']')[0] + ']', value=hajime_card[3].split(']')[1])
      webhook_c.webhook_send(webhook.url)

   @commands.command('webtes')
   async def webhook_test(self, ctx):
      webhook_c = Webhook_Control()
      webhook = await webhook_c.get_webhook(ctx)
      webhook_url = webhook.url
      urls = []
      with open('json/gif_url.json', 'r')as f:
         gif = json.load(f)
      urls = random.sample(gif['HAJIME'], 4)
      webhook_c.image_add(urls)
      webhook_c.add_title(title='わっほーい！')
      webhook_c.webhook_send(webhook_url)
      await asyncio.sleep(3)
      # async for log in ctx.channel.history(limit=10):
      #    if log.author.id==webhook.id:
      #       await log.delete()
      #       break

   @commands.command('apites')
   async def webhook_test2(self, ctx, idol_name: str = '神谷奈緒'):
      webhook_c = Webhook_Control()
      webhook = await webhook_c.get_webhook(ctx)
      webhook_url = webhook.url
      urls = []
      idol = self.db.select(
          f'select *from idol_data where name="{idol_name}"')[0]
      tall = idol['height']
      webhook_c.add_field(name="属性", value=f"{idol['element']}", inline=False)
      webhook_c.add_field(name="年齢", value=f"{idol['age']}")
      webhook_c.add_field(name="身長", value=f"{tall}cm")
      webhook_c.add_field(name="誕生日", value=f"{idol['birthday']}")
      webhook_c.add_field(name="出身地", value=f"{idol['birthplace']}")
      webhook_c.add_field(name="血液型", value=f"{idol['blood_type']}")
      webhook_c.add_field(name="利き手", value=f"{idol['hand']}")
      webhook_c.add_field(name="趣味", value=f"{idol['hobby']}")
      webhook_c.add_field(name="奈緒との身長差", value=f"{tall-154}cm")
      with open('json/idol_data.json', 'r')as f:
         idol_data = json.load(f)
      idols = [x for x in idol_data['result'] if x['name_only'] == idol_name]
      ids = [x['id'] for x in idols]
      ids += [x['id'] + 1 for x in idols]
      ids = random.sample(ids, 4)
      for id in ids:
         url = f'https://starlight.kirara.ca/api/v1/card_t/{id}'
         r = requests.get(url)
         urls.append(r.json()['result'][0]['spread_image_ref'])

      webhook_c.image_add(urls)
      webhook_c.add_title(title=idol_name)
      webhook_c.webhook_send(webhook_url)

   @commands.command("ガシャ")
   async def gasya(self, ctx):
      with open('text/newcard.csv')as f:
         reader = csv.reader(f)
         cards = [row for row in reader]
         card = random.choice(cards)
         embed = discord.Embed(title=f"{card[3]}", url=f"https://pink-check.school/card/detail/{card[1]}")
         embed.set_image(
             url=f'https://pink-check.school/image/withoutsign/{card[1]}')
         embed.add_field(name="コスト", value=f"{card[15]}")
         embed.add_field(name="攻", value=f"{card[18]}")
         embed.add_field(name="守", value=f"{card[19]}")
         if card[21] != '':
            embed.add_field(
                name=f"特技「{card[20]}」",
                value=f"{card[21]}",
                inline=False)
         await ctx.send(embed=embed)

   @commands.command("納税")
   async def tax(self, ctx):
      url = "https://starlight.kirara.ca/api/v1/list/card_t"
      idols_data = requests.get(url).json()
      idols = [x for x in idols_data['result']]
      idol = random.choice(idols)
      url = f'https://starlight.kirara.ca/api/v1/card_t/{idol["id"]}'
      idol = requests.get(url).json()
      embed = discord.Embed(title=f"{idol['result'][0]['name']}")
      embed.set_image(url=idol['result'][0]['card_image_ref'])
      embed.add_field(name="Vo", value=f"{idol['result'][0]['vocal_max']}")
      embed.add_field(name="Da", value=f"{idol['result'][0]['dance_max']}")
      embed.add_field(name="Vi", value=f"{idol['result'][0]['visual_max']}")
      embed.add_field(name=f"センター効果「{idol['result'][0]['lead_skill']['name']}」", value=f"{idol['result'][0]['lead_skill']['explain']}",inline=False)
      embed.add_field(name=f"特技「{idol['result'][0]['skill']['skill_name']}」", value=f"{idol['result'][0]['skill']['explain']}")
      await ctx.send(embed=embed)


   @commands.command("カード検索")
   async def cards(self, ctx, name: str):
      card_list = []
      card_list_evolution = []
      with open('text/newcard.csv')as f:
         reader = csv.reader(f)
         cards = [row for row in reader]
         for card in cards:

            if name == card[6]:
               card_list = []
               card_list.append(card[3])
               card_list_evolution.append(card[3] + '+')
               break
            elif name in card[3] and card[3][-1] != '+':
               card_list.append(card[3])
            elif name in card[3] and card[3][-1] == '+':
               card_list_evolution.append(card[3])

         if len(card_list) > 10:
            await ctx.send('該当カードが多いのでもう少し絞ってね')
         elif len(card_list) > 1:
            embed = discord.Embed(title="複数見つかりました", description="選んでください")
            for card in card_list:
               embed.add_field(name="カード名", value=f"{card}")
            await ctx.send(embed=embed)

         elif len(card_list) == 1:
            card = [x for x in cards if x[3] == card_list[0]][0]
            card2 = [x for x in cards if x[3] == card_list_evolution[0]][0]
            webhook_c = Webhook_Control()
            webhook = await webhook_c.get_webhook(ctx)
            webhook_url = webhook.url
            urls = [
                f'https://pink-check.school/image/withoutsign/{card[1]}',
                f'https://pink-check.school/image/withoutsign/{card2[1]}']
            webhook_c.image_add(urls)
            webhook_c.add_title(title=f"{card[3]},{card2[3]}")
            webhook_c.add_field(name="コスト", value=f"{card[15]}")
            webhook_c.add_field(name="攻", value=f"{card[18]}")
            webhook_c.add_field(name="守", value=f"{card[19]}")
            if card[21] != '':
               webhook_c.add_field(
                   name=f"特技「{card[20]}」",
                   value=f"{card[21]}",
                   inline=False)
            webhook_c.add_field(name="コスト", value=f"{card2[15]}")
            webhook_c.add_field(name="攻", value=f"{card2[18]}")
            webhook_c.add_field(name="守", value=f"{card2[19]}")
            if card2[21] != '':
               webhook_c.add_field(
                   name=f"特技「{card2[20]}」",
                   value=f"{card2[21]}",
                   inline=False)
            webhook_c.webhook_send(webhook_url)
         else:
            await ctx.send("見つかりませんでした")


def setup(bot):
   bot.add_cog(Idol(bot))
