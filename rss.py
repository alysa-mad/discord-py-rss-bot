import discord
import feedparser
import os
import asyncio

looking = False
listrss = []
listrss_mdan = []
listrss_shakaw = []
old_mdan = []
old_mdan.append("0")
old_mdan.append("1")
msg_mdan = False
old_shakaw = []
old_shakaw.append("0")
old_shakaw.append("1")
msg_shakaw = False
d = feedparser.parse('RSS_MDAN')
s = feedparser.parse('RSS_SHAKAW')
client = discord.Client()

@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global looking
    global old_mdan
    global msg
    link_mdan = d.entries[0].link
    link_shakaw = s.entries[0].link
    if message.author == client.user:
        return
    if message.content == "$look":
        looking = True
        print("[Debug]Valor de old_mdan[1]:", old_mdan[1])
        print("[Debug]Valor de old_shakaw[1]:", old_shakaw[1])
    if message.content == "$stop":
        msg_mdan = False
        msg_shakaw = False
        looking = False
        print("[Debug] Você parou!")
        await message.channel.send("Você parou!")
    if message.content == "$restart":
        print("[Debug] Você recomeçou a procura!")
        await message.channel.send("Você recomeçou a procura!")
        msg_mdan = True
        msg_shakaw = True
        looking = True
        print("[Debug]Valor de old_mdan[1]:", old_mdan[1])
        print("[Debug]Valor de old_shakaw[1]:", old_shakaw[1])
    while looking:
        while msg_mdan:
            if await looking_mdan(old_mdan[1]) == False:
                print("[Debug] Sem atualizações ainda na Shakaw!")
                break
            else:
                desc = d.entries[0].description
                listrss_mdan.append(d.entries[0].title)
                listrss_mdan.append(d.entries[0].link)
                listrss_mdan.append(desc.replace("<br />", "-").replace("[img]", "").replace("[/b]", "").replace("[b]", "").replace("[/img]", ""))
                listrss.append(listrss_mdan)
                for i in range(len(listrss[0])):
                    await message.channel.send(listrss[0][i])
                old_mdan.clear()
                old_mdan = listrss[0][1].copy()
                print("[Debug]Valor de f'old[1]:", old[1])
                listrss.clear()
                looking = True
                msg = False
        while msg_shakaw:
            if await looking_shakaw(old_shakaw[1]) == False:
                print("[Debug] Sem atualizações ainda na Shakaw!")
                break
            else:
                desc = d.entries[0].description
                listrss_shakaw.append(d.entries[0].title)
                listrss_shakaw.append(d.entries[0].link)
                listrss_shakaw.append(desc.replace("<br />", "-").replace("[img]", "").replace("[/b]", "").replace("[b]", "").replace("[/img]", ""))
                listrss.append(listrss_shakaw)
                for e in range(len(listrss[1])):
                    await message.channel.send(listrss[1][e])
                old.clear()
                old = listrss[0][1].copy()
                print("[Debug] Valor de f'old_shakaw[1]:", old[1])
                listrss.clear()
                looking = True
                msg = False

async def looking_mdan(input_link):    ## Define qual RSS será atualizado
    link_mdan = d.entries[0].link
    if input_link == link_mdan:
        await asyncio.sleep(4)
        print("[Debug] Sem atualizações ainda na Mdan!")
        return False
    else:
        print("[Debug] Atualização Encontrada na Mdan!")
        await message.channel.send("Atualização Encontrada na Mdan!")
        return True

async def looking_shakaw(input_link):    ## Define qual RSS será atualizado
    link_shakaw = s.entries[0].link
    if input_link == link_shakaw:
        await asyncio.sleep(4)
        print("[Debug] Sem atualizações ainda na Shakaw!")
        return False
    else:
        print("[Debug] Atualização Encontrada na Shakaw!")
        await message.channel.send("Atualização Encontrada na Shakaw!")
        return True
    print("[Debug] message.content final de loop 1", message.content)
client.run('Discord_BOT_TOKEN')
