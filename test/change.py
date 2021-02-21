import json
with open("picture.json","r")as f:
   dic=json.load(f)
dic["バジリスク"] = 2
dic["デレステコラ"] = 3
dic["優しい世界観"] = 4
dic["全員アウト"]=5
dic["nhk"]=6


with open("picture.json","w")as f:
    json.dump(dic, f, indent=3)