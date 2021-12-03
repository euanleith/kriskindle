import random
import traceback
import discord
import emoji
import requests
import numpy as np
import pickle

DISCORD_TOKEN = '<token>' # find here: https://discord.com/developers/applications/783103691036557362/bot
TENOR_TOKEN = '6RBF86B3QSNB'
GIFS = np.array(['floppa', 'sogga', 'venti', 'thoma', 'diluc', 'amongus', 'femboy', 'malewife', 'doge', 'frog',
                 'peepo', 'pepe', 'horny jail', 'crazy frog'])
participants = pickle.load(open('tuple.dump', 'rb'))

client = discord.Client()

def assign(participants):
    while True:
        rand = random.sample(participants, len(participants))
        cont = False
        for r, p in zip(rand, participants):
            if r == p:
                cont = True
                break
        if not cont:
            return rand

def getGif(searchTerm):
    response = requests.get("https://g.tenor.com/v1/search?q={}&key={}".format(searchTerm, TENOR_TOKEN))
    data = response.json()
    randIndex = random.randint(0, len(data['results'])-1)
    url = data['results'][randIndex]['media'][0]['gif']['url']
    embed = discord.Embed()
    embed.set_image(url=url)
    return embed

def randEmoji(client):
    randIndex = random.randint(0, len(client.emojis)-1)
    return client.emojis[randIndex]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    try:
        if message.content.startswith('-join'):
            author = (message.author.id, message.author.nick)
            if author in participants:
                await message.channel.send('get away from me aha x')
            else:
                participants.append(author)
                await message.channel.send('welcome to the broth, ' + str(message.author) + ' ' + str(randEmoji(client)))
                pickle.dump(participants, open('tuple.dump', 'wb'))
            await message.channel.send(embed=getGif(np.random.choice(GIFS)))
        elif message.content.startswith('-leave'):
            author = (message.author.id, message.author.nick)
            participants.remove(author)
            await message.channel.send('very cool, unfortunately i have had intercourse with your mother ' + str(randEmoji(client)))
            await message.channel.send(embed=getGif(np.random.choice(GIFS)))
            pickle.dump(participants, open('tuple.dump', 'wb'))
        elif message.content.startswith('-run'):
            if len(participants) < 2:
                await message.channel.send('get more friends ' + str(randEmoji(client)))
            else:
                await message.channel.send('besties... attack! ' + str(randEmoji(client)))
                rand = assign(participants)
                for p, r in zip(participants, rand):
                    user = await client.fetch_user(p[0])
                    await user.send('You got ' + str(r[1]) + '!!!')
                    await user.send(embed=getGif(np.random.choice(GIFS)))
            await message.channel.send(embed=getGif(np.random.choice(GIFS)))
        elif message.content.startswith('-list'):
            await message.channel.send([p[1] for p in participants])
            await message.channel.send(embed=getGif(np.random.choice(GIFS)))
        elif message.content.startswith('-clear'):
            await message.channel.send('mfw genocide ' + str(randEmoji(client)))
            await message.channel.send(embed=getGif(np.random.choice(GIFS)))
            participants.clear()
    except:
        await message.channel.send('ruh roh, someone did a stinky ' + emoji.emojize(":point_right:") + emoji.emojize(":point_left:"))
        traceback.print_exc()


client.run(DISCORD_TOKEN)
