import sqlite3
import csv
with (sqlite3.connect("db/bot_data.db")) as conn:
   c = conn.cursor()
   with open("dere_profil.csv") as f:
      text = [row for row in csv.reader(f)]
      for i in text:
         num=int(i[8].replace("cm",""))
         if i[0]=="":
            c.execute(f'update idol_data set height={num} where name="{i[1]}"')
         else:
            c.execute(f'update idol_data set height={num} where name="{i[0]}{i[1]}"')
         conn.commit()
    
 