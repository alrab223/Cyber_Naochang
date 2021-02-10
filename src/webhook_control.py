import requests
import json
class Webhook_Control:

   def __init__(self):
      with open('json/webhook.json','r')as f:
         self.params=json.load(f)

   def image_add(self,urls:list):
      
      for i, url in enumerate(urls):
         self.params['embeds'][i]['image']['url']=urls[i]
   
   def add_title(self,title=None,description=None,color=None):
      self.params['embeds'][0]['title']=title
      self.params['embeds'][0]['description']=description
      self.params['embeds'][0]['color']=color
   
   def add_field(self,name=None,value=None,inline=True):
      field={"name": name,"value": value,"inline": inline}
      if not 'fields' in self.params['embeds'][0]:
         self.params['embeds'][0]['fields']=[]
      self.params['embeds'][0]['fields'].append(field)
   
   def webhook_send(self,url):
      requests.post(url,json.dumps(self.params),headers={'Content-Type': 'application/json'})
    
      
      