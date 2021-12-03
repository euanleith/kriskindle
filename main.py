import random
import traceback
import discord
import emoji
import requests
import numpy as np
import pickle

DISCORD_TOKEN = 'NzgzMTAzNjkxMDM2NTU3MzYy.X8V4JQ.ztSt-wUs-bOFFFpADWRqzajZTOA'
TENOR_TOKEN = '6RBF86B3QSNB'
GIFS = np.array(['floppa', 'sogga', 'venti', 'thoma', 'diluc', 'amongus', 'femboy', 'malewife', 'doge', 'frog',
                 'peepo', 'pepe', 'horny jail', 'crazy frog'])
participants = pickle.load(open('tuple.dump', 'rb'))
wishlists = pickle.load(open('wishlists.dump', 'rb'))

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
    randIndex = random.randint(0, len(data['results']) - 1)
    url = data['results'][randIndex]['media'][0]['gif']['url']
    embed = discord.Embed()
    embed.set_image(url=url)
    return embed


def randEmoji(client):
    randIndex = random.randint(0, len(client.emojis) - 1)
    return client.emojis[randIndex]


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    try:
        if message.content.startswith('-'):
            content = message.content[1:]
            out = ''
            if content == 'help':
                out = 'commands:\n' \
                      '-join: add yourself to kriskindle\n' \
                      '-leave: leave\n' \
                      '-run: start the games\n' \
                      '-list: list participants\n' \
                      '-wishlist: see your wishlist\n' \
                      "-wishlist <name>: see <name>'s wishlist\n" \
                      '-wishlist add: add to your wishlist\n' \
                      '-wishlist remove: remove from your wishlist\n' \
                      '-wishlist clear: clear your wishlist\n'
            elif content == 'join':
                author = (message.author.id, message.author.nick)
                if author in participants:
                    out = 'get away from me aha x'
                else:
                    participants.append(author)
                    wishlists[author[1]] = list()
                    out = 'welcome to the broth, ' + str(message.author)
                    pickle.dump(participants, open('tuple.dump', 'wb'))
                    pickle.dump(wishlists, open('wishlists.dump', 'wb'))
            elif content == 'leave':
                author = (message.author.id, message.author.nick)
                participants.remove(author)
                del wishlists[author[1]]
                out = 'very cool, unfortunately i have had intercourse with your mother'
                pickle.dump(participants, open('tuple.dump', 'wb'))
            elif content.startswith('kick'):
                if content[5:] in wishlists:
                    [participants.remove(p) for p in participants if p[1] == content[5:]]
                    del wishlists[content[5:]]
                    out = 'the daemon ' + content[5:] + ' has been excised'
                else:
                    out = 'who tf is ' + content[5:] + ' frfr'
            elif content == 'run':
                if len(participants) < 2:
                    out = 'get more friends'
                else:
                    out = 'besties... attack!'
                    rand = assign(participants)
                    for p, r in zip(participants, rand):
                        user = await client.fetch_user(p[0])
                        await user.send('You got ' + str(r[1]) + '!!!')
                        await user.send(embed=getGif(np.random.choice(GIFS)))
            elif content == 'list':
                out = [p[1] for p in participants]
            elif content == 'clear':
                out = 'mfw genocide'
                participants.clear()
            elif content.startswith('wishlist'):
                author = (message.author.id, message.author.nick)
                if not author[1] in wishlists:
                    out = 'you do not exist'
                else:
                    # todo if run has been done, user should be able to easily find the wishlist of the person they got without inputting their name
                    msg = content[8:]
                    if msg == '':
                        if len(wishlists[author[1]]) == 0:
                            out = 'ERROR MUNGUS NOT FOUND'
                        else:
                            out = wishlists[author[1]]
                    elif msg.startswith(' add'):
                        wishlists[author[1]].append(content[14:])
                        out = "added " + content[14:]
                    elif msg.startswith(' remove'):
                        if content[17:] not in wishlists[author[1]]:
                            out = "didn't find " + content[17:]
                        else:
                            wishlists[author[1]].remove(content[17:])
                            out = "removed " + content[17:]
                    elif msg == ' clear':
                        wishlists[author[1]] = list()
                        out = 'the deed has been done'
                    elif msg[1:] in wishlists:
                        if len(wishlists[msg[1:]]) == 0:
                            out = 'ERROR MUNGUS NOT FOUND'
                        else:
                            out = wishlists[msg[1:]]
                    else:
                        out = 'who tf is' + msg + ' frfr'
                    pickle.dump(wishlists, open('wishlists.dump', 'wb'))
            else:
                await message.channel.send('wot tf u on about matey alri ya')
            await message.channel.send(str(out) + ' ' + str(randEmoji(client)))
            await message.channel.send(embed=getGif(np.random.choice(GIFS)))

    except:
        await message.channel.send(
            'ruh roh, someone did a stinky ' + emoji.emojize(":point_right:") + emoji.emojize(":point_left:"))
        traceback.print_exc()


client.run(DISCORD_TOKEN)
