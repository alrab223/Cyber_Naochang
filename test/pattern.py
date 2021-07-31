with open('../text/uwasa.txt')as f:
   text_list = f.readlines()
dic = {}
text = ''
idol = ''
count = 0
for i in text_list:
   if 'のウワサ' in i:
      if count != 0:
         text=text.replace('\n','')
         dic[f'{idol}'].append(text)
         text=''
      idol = i.split("のウワサ")[0]
      if idol not in dic:
         dic[f'{idol}'] = []
   else:
      text += i
   count+=1
print(dic)
