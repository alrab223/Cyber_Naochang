from matplotlib import pyplot as plt
from random import randint
import sqlite3
# データの定義(サンプルなのでテキトー)
year = []
month = []
day = []
count = 0
x = []
y=[]
with (sqlite3.connect("bot_data.db")) as conn:
      c = conn.cursor()
      c.execute(f'select year,month,day from user_join')
gold = c.fetchall()
gold.sort()
for i in gold:
   year.append(i[0])
   if i[0]==2020:
      month.append(str(i[1]) + "_2020")
   else:
      month.append(str(i[1]))
   day.append(i[2])
   print(i)
first=str(month[0])
for i in month:
   if i == first:
      count += 1
   else:
      x.append(first)
      y.append(count)
      count+=1
      first=i
      

plt.xticks(rotation=40)
plt.plot(x, y)
plt.show()