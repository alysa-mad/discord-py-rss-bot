import discord
import feedparser
import os
import asyncio

looking = True
listrss = []
old = []
old.append("0")
old.append("1")
msg = False
d = feedparser.parse('RSS_MDAN')
client = discord.Client()

@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global looking
    global old
    global msg
    link = d.entries[0].link
    if message.author == client.user:
        return
    if message.content == "$mdan":
        msg = True
        looking = True
        print("[Debug]Valor de old[1]:", old[1])
    if message.content == "$stop":
        msg = False
        looking = False
        print("[Debug] Você parou!")
        await message.channel.send("Você parou!")
    if message.content == "$restart":
        print("[Debug] Você recomeçou a procura!")
        await message.channel.send("Você recomeçou a procura!")
        msg = True
        looking = True
        print("[Debug]Valor de old[1]:", old[1])

    while looking:
        while looking:
            print("[Debug] Valor variável looking: ", looking)
            if old[1] == link:
                msg = False
                await asyncio.sleep(4)
                print("[Debug] Sem atualizações ainda!")
            else:
                msg = True
                print("[Debug] Atualização Encontrada!")
                await message.channel.send("Atualização Encontrada!")
                looking = False
        while msg:
            if old[1] == link:
                msg = False
                print("[Debug] Sem atualizações ainda!")
            else:
                desc = d.entries[0].description
                listrss.append(d.entries[0].title)
                listrss.append(d.entries[0].link)
                listrss.append(desc.replace("<br />", "-").replace("[img]", "").replace("[/b]", "").replace("[b]", "").replace("[/img]", ""))
                for i in range(len(listrss)):
                    await message.channel.send(listrss[i])
                old.clear()
                old = listrss.copy()
                print("[Debug]Valor de f'old[1]:", old[1])
                listrss.clear()
                looking = True
                msg = False
    print(message.content)
client.run('Discord_BOT_TOKEN')
