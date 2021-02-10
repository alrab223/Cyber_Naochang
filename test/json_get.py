import requests
import pprint
import json
import time 
# url = 'https://starlight.kirara.ca/api/v1/skill_t/200571'

# params={'ref': '/api/v1/skill_t/200571'}
# r = requests.get(url,params=params)

# print(r.text)
with open('../json/idol_data.json')as f:
   idol=json.load(f)
idols=[x for x in idol['result'] if x['name_only']=='神谷奈緒']
ids=[x['id'] for x in idols]
for id in ids:
   url = f'https://starlight.kirara.ca/api/v1/card_t/{id}'
   r = requests.get(url)
   print(r.json())
   time.sleep(0.5)
