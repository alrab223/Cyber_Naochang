import csv
import mojimoji
with open('../text/Card.csv')as f:
   reader=csv.reader(f)
   l = [row for row in reader]
   with open('../text/newcard.csv','w') as s:
      for i in l:
         i[3]=mojimoji.han_to_zen(i[3], digit=False,ascii=False)
         writer = csv.writer(s)
         writer.writerow(i)