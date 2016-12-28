import discord
import asyncio
import random
from cleverbot import Cleverbot
import pyowm
import json
import wikipedia


def find_emoji(toFind, emojis):
    for emoji in emojis:
        if emoji.name==toFind:
            return emoji
def chunkstring(string, length):
    return list(string[0+i:length+i] for i in range(0, len(string), length))

r=random.Random()
client = discord.Client()
cb = Cleverbot()
owm = pyowm.OWM('b75f0949afe7dbabc3312f283c4a11c4')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    print(message.author.name + ': ' + message.content)

    if message.content.startswith('!game'):
        try:
            await client.send_message(message.channel,"You are playing: " + message.author.game.name)
        except:
            await client.send_message(message.channel,"You are playing with yourself")
    elif message.content.startswith('!dice'):
        try:
            size = int(message.content[5:message.content.index(' ')])
        except:
            size = int(message.content[5:])
        out = int(r.random()*size + 1)
        if size == 0:
            await client.send_message(message.channel,"Error")
        else:
            await client.send_message(message.channel,"You rolled a " + str(out))
    elif message.content.startswith('!cleverbot'):
        toAsk=message.content[10:]
        await client.send_message(message.channel,cb.ask(toAsk))
    elif message.content.startswith('!weather'):
        obs=owm.weather_at_id(4180439)
        w=obs.get_weather()
        temp = w.get_temperature('fahrenheit')
        output = ("The temperature in Atlanta is " + str(temp['temp']) +
        "\u00B0")
        await client.send_message(message.channel,output)
    elif message.content.startswith('!wikipedia'):
        toAsk=message.content[10:]
        try:
            out = wikipedia.summary(wikipedia.search(toAsk)[0])
            for i in chunkstring(out,2000):
                await client.send_message(message.channel,i)
        except:
            await client.send_message(message.channel,"Bad search term")
    elif message.content.startswith('!help'):
        out = ("\u2063\n**!dice###:** replace number signs with the dice size. Returns the result of a rolled dice of specified size"
               + "\n**!cleverbot [message]:** sends a message to cleverbot, respods with the response"
               + "\n**!weather:** returns the current temperature in Atlanta."
               + "\n**!wikipedia [search term]:** returns a wikipedia summary of the search term"
               + "\n**!game:** tells people what game you are playing")
        await client.send_message(message.channel,out)
    if 'fuck' in message.content.lower():
        await client.add_reaction(message,find_emoji("no",client.get_all_emojis()))
    """if message.author.id != "145616998611681280":
        rand = r.random()*100
        print('insult ' + str(int(rand)))
        if int(rand) <= 2:
            await client.send_message(message.channel,"<@"+message.author.id+">, you're a piece of shit")"""



client.run('MjU4NzM5NDU0OTkzMzY3MDQx.CzTmsA.XHFDJJIst_sMBTDIY1B6DyqxqDI')
