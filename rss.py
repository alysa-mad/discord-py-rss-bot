import discord
import feedparser
import os
import time
import asyncio

looking = True
listrss = []
old = []
old.append("nothing")
old.append("1")
msg = False
d = feedparser.parse('https://bt.mdan.org/rss.php?cats=1,2,3,4,5,6,7,13,18,20,22,24&passkey=d2ad6f0ed6ce5a64c8f96518286718df')
client = discord.Client()

@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global old
    global msg
    link = d.entries[0].link
    if message.author == client.user:
        return
    if message.content.startswith("$mdan"):
        msg = True
        looking = True
        print(old[1])
    if message.content.startswith("$mdan stop"):
        msg = False
        looking = False
        print("Você parou!")
    while True:
        while looking:
            if old[1] == link:
                msg = False
                await asyncio.sleep(4)
                print("Sem atualizações ainda!")
                looking = True
            else:
                msg = True
                print("Atualização Encontrada!")
                await message.channel.send("Atualização Encontrada!")
                looking = False
        while msg:
            if old[1] == link:
                msg = False
                print("Sem atualizações ainda!")
                looking = True
            else:
                desc = d.entries[0].description
                listrss.append(d.entries[0].title)
                listrss.append(d.entries[0].link)
                listrss.append(desc.replace("<br />", "-").replace("[img]", "").replace("[/b]", "").replace("[b]", "").replace("[/img]", ""))
                for i in range(len(listrss)):
                    await message.channel.send(listrss[i])
                old.clear()
                old = listrss.copy()
                print(old[1])
                listrss.clear()
                looking = True
                msg = False

client.run('Discord_BOT_TOKEN')
