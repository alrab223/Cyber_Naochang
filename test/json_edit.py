import json
with open("emoji.json","r")as f:
    dic=json.load(f)
dic["rainbow_art"] = [754617911888314388,754620925873356910,754620976116924426,754621022497669190,754621024703741964,754621031377010699,754621042600706048]
with open("emoji.json","w")as f:
    json.dump(dic, f, indent=3)