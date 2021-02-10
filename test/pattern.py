import re

pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
text: list = re.findall(pattern, "https://t.co/xvlx7IOl6p")
print(text)