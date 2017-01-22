import discord
import asyncio
import random
from cleverbot import Cleverbot
import pyowm
import json
import wikipedia
import markovify
import glob


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

token = open('config/discordtoken.txt')
token = token.read()

markovModels = {}
for path in glob.glob('logs/*'):
    name = path[5:path.index('.')]
    
    file = open(path,'r')
    toParse = file.read()
    markovModels[name] = markovify.NewlineText(toParse)


@client.event
async def on_ready():
    global markovModels
    print('getting chatlogs, this may take a bit')
    logs1 = client.logs_from(client.get_channel('258691524471160832'),limit=99999)
    logs2 =client.logs_from(client.get_channel('145617304472911872'),limit=99999)
    logs3 =client.logs_from(client.get_channel('233372734195761154'),limit=99999)
    logFile = open('logs/chatlogs.txt','w')
    messageByAuthor = {}
    async for item in logs1:
        try:
            messageByAuthor[item.author.id].append(item.content + '\n')
        except:
            messageByAuthor[item.author.id]=[]
            messageByAuthor[item.author.id].append(item.content + '\n')
    async for item in logs2:
        try:
            messageByAuthor[item.author.id].append(item.content + '\n')
        except:
            messageByAuthor[item.author.id]=[]
            messageByAuthor[item.author.id].append(item.content + '\n')
    async for item in logs3:
        try:
            messageByAuthor[item.author.id].append(item.content + '\n')
        except:
            messageByAuthor[item.author.id]=[]
            messageByAuthor[item.author.id].append(item.content + '\n')
    for path in glob.glob('logs/*'):
        name = path[5:path.index('.')]
    
        file = open(path,'r')
        toParse = file.read()
        markovModels[name] = markovify.NewlineText(toParse)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

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
               + "\n**!game:** tells people what game you are playing"
               + "\n**!potato [@user]:** the bot tries to immitate us")
        await client.send_message(message.channel,out)
    elif message.content.startswith('!logs'):
        print('getting chatlogs, this may take a bit')
        logs1 = client.logs_from(client.get_channel('258691524471160832'),limit=99999)
        logs2 =client.logs_from(client.get_channel('145617304472911872'),limit=99999)
        logFile = open('logs/chatlogs.txt','w')
        messageByAuthor = {}
        async for item in logs1:
            try:
                messageByAuthor[item.author.id].append(item.content + '\n')
            except:
                messageByAuthor[item.author.id]=[]
                messageByAuthor[item.author.id].append(item.content + '\n')
        async for item in logs2:
            try:
                messageByAuthor[item.author.id].append(item.content + '\n')
            except:
                messageByAuthor[item.author.id]=[]
                messageByAuthor[item.author.id].append(item.content + '\n')
        
        for iteml in messageByAuthor.keys():
            file = open('logs/'+iteml+'.txt','w')
            for item in messageByAuthor[iteml]:
                try:
                    file.write(item)
                    logFile.write(item)
                except:
                    pass
            file.close()
        print('done')
    elif message.content.startswith('!potato'):
        print(print(message.content))
        if '@' in message.content:
            param= message.content[10:message.content.index('>')]
            output = markovModels[param.replace('!','')].make_sentence()
            print(param, output)
            count = 15
            while output == None and count<=100:
                output = markovModels[param.replace('!','')].make_sentence(tries=count)
                count+=5
                print(param, output)
            if output == None:
                output = 'Markov Failed.'
        else:
            output = markovModels['chatlogs'].make_sentence()
            print('fail')
        await client.send_message(message.channel,output)
    """if 'fuck' in message.content.lower():
        await client.add_reaction(message,find_emoji("no",client.get_all_emojis()))"""
    """if message.author.id != "145616998611681280":
        rand = r.random()*100
        print('insult ' + str(int(rand)))
        if int(rand) <= 2:
            await client.send_message(message.channel,"<@"+message.author.id+">, you're a piece of shit")"""



client.run(token)
