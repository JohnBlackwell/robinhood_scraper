from bs4 import BeautifulSoup
from twilio.rest import Client
import decimal
from urllib.request import urlopen
import re 
import os
from dotenv import load_dotenv

load_dotenv()

min = os.getenv('MIN')
max = os.getenv('MAX')

url = "https://robinhood.com/stocks/PEIX"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")


text = soup.get_text() 
s = re.search('\d+\.\d+', text).group(0)
d = decimal.Decimal(s)

b = ""
if d <= decimal.Decimal(min) or d >= decimal.Decimal(max):
     b = "Sell PEIX Stock"
else:
     b = "Keep PEIX Stock"


account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
origin = os.getenv('ORIGIN_NUMBER')
dest = os.getenv('DEST_NUMBER')

client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body=b,
         from_=origin,
         to=dest
     )

print(message.sid)