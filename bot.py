# bot.py
import json
import os
import random

import discord
from discord.ext import tasks
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup as parse

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANEL_ID = os.getenv('DISCORD_CHANEL_ID')

# Opening JSON file
f = open('greetings.json')
  
# returns JSON object as 
# a list
GREETINGS = json.load(f)

def parse_predicttion(prediction_sign: str):
    url = "https://horo.mail.ru/prediction/{sign}/today/".format(sign=prediction_sign)
    r = requests.get(url)
    parse1 = parse(r.content, 'html.parser')

    return parse1.find(class_="article__item article__item_alignment_left article__item_html").text.strip()

client = discord.Client()
   
@tasks.loop(hours=24)
async def backgorund_task():
    await client.wait_until_ready()
    channel = client.get_channel(id=int(DISCORD_CHANEL_ID)) # replace with channel_id
    
    sign_list = {
        "aries": "Овны ♈:",
        "taurus": "Телцы ♉:",
        "gemini": "Близнецы ♊:",
        "cancer": "Раки ♋:",
        "leo": "Львы ♌:",
        "virgo": "Девы ♍:",
        "libra": "Весы ♎:",
        "scorpio": "Скорпионы ♏:",
        "sagittarius": "Стрелцы ♐:",
        "capricorn": "Козероги ♑:",
        "aquarius": "Водолеи ♒:",
        "pisces": "Рыбы ♓:"
    }

    
    msg = random.choice(GREETINGS) + "\n"
    predictions = []
    
    for sign in sign_list:
        predictions.append(sign_list[sign] + "\n" + parse_predicttion(sign) + "\n\n")
    
    await channel.send(msg)
    for prediction in predictions:
        await channel.send(prediction)
    
    
    

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

backgorund_task.start()
client.run(TOKEN)