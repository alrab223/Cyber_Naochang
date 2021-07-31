import json
with open('../json/picture.json','r')as f:
   pic=json.load(f)
print(pic)