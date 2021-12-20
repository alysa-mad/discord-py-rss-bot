import discord
import feedparser
import os
import asyncio

call_link = False
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
passk = None
d = feedparser.parse('RSS_MDAN')
s = feedparser.parse('RSS_SHAKAW')
client = discord.Client()

@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global looking
    global call_link
    global passk
    global old_mdan
    global old_shakaw
    global msg_mdan
    global msg_shakaw
    link_mdan = d.entries[0].link
    title_shakaw = s.entries[0].title
    if message.author == client.user:
        return
    if message.content == "$look":
        msg_mdan = True
        msg_shakaw = True
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
    if message.content == "$pass":
        await message.author.send("Escreva sua chave Shakaw: (Por sua segurança edite a mensagem após o envio!)")
        def check(m):
                    return m.author == message.author
        msg = await client.wait_for('message', check=check)
        passk = msg.content
        try:
            storage_pass.pop(message.author)
        except:
            continue
        storage_pass = {message.author: msg.content}
        print(storage_pass.get(message.author))
        await message.author.send("Sua chave foi armazenada!")
    if message.content == "$link":
        call_link = True
    while looking:
        print("[Debug] Test while 1")
        while msg_mdan:
            print("[Debug] Test while 2")
            try:
                if await looking_mdan(old_mdan[1]) == False:
                    print("[Debug] Sem atualizações ainda na Mdan [1]while msg_m!")
                    break
                else:
                    await message.channel.send("Atualização Encontrada na Mdan [1]while msg_m!")
                    desc_m = d.entries[0].description
                    listrss_mdan.append(d.entries[0].title)
                    listrss_mdan.append(d.entries[0].link)
                    listrss_mdan.append(desc_m.replace("<br />", "-").replace("[img]", "").replace("[/b]", "").replace("[b]", "").replace("[/img]", ""))
                    listrss.append(listrss_mdan)
                    for i in range(len(listrss[0])):
                        await message.channel.send(listrss[0][i])
                    old_mdan.clear()
                    old_mdan = listrss[0].copy()
                    print("[Debug]Valor de f'old_mdan[1]:", old_mdan[1])
                    listrss.clear()
                    break
            except IndexError:
                print("[DEBUG] RSS MDAN Indisponível - Erro de Conexão")
                continue
        while msg_shakaw:
            if call_link:
                linkcallsk = s.entries[0].link
                linkcallsk = linkcallsk.split("passkey=", 2)
                if passk != None:
                    linkcallsk = linkcallsk[0] + "passkey=" + passk
                    await message.author.send(linkcallsk)
                else:
                    linkcallsk = "---- Passkey não recebida, use $pass ----"
                    await message.channel.send(linkcallsk)
                call_link = False
            try:
                if await looking_shakaw(old_shakaw[0]) == False:
                    print("[Debug] Sem atualizações ainda na Shakaw [1]while msg_s!")
                    break
                else:
                    await message.channel.send("Atualização Encontrada na Shakaw")
                    listrss_shakaw.append(s.entries[0].title)
                    linksk = s.entries[0].link
                    linksk = linksk.split("passkey=", 2)
                    if passk != None:
                        linksk = linksk[0] + "passkey=" + passk
                    else:
                        linksk = "---- Passkey não recebida, use $pass ----"
                    listrss_shakaw.append(linksk)
                    listrss.append(listrss_shakaw)
                    for e in range(len(listrss[0])):
                        await message.channel.send(listrss[0][e])
                    old_shakaw.clear()
                    old_shakaw = listrss[0].copy()
                    print("[Debug] Valor de f'old_shakaw[1]:", old_shakaw[1])
                    listrss.clear()
                    break
            except IndexError:
                print("[DEBUG] RSS Shakaw Indisponível - Erro de Conexão")
                continue
async def looking_mdan(input_link):    ## Define qual RSS será atualizado
    link_mdan = d.entries[0].link
    if input_link == link_mdan:
        await asyncio.sleep(4)
        print("[Debug] Sem atualizações ainda na Mdan [2]func_m!")
        return False
    else:
        print("[Debug] Atualização Encontrada na Mdan [2]func_m!")
        return True

async def looking_shakaw(input_link):    ## Define qual RSS será atualizado
    title_shakaw = s.entries[0].title
    if input_link == title_shakaw:
        await asyncio.sleep(4)
        print("[Debug] Sem atualizações ainda na Shakaw [2]func_s!")
        return False
    else:
        print("[Debug] Atualização Encontrada na Shakaw [2]func_s!")
        return True
    print("[Debug] message.content final de loop 1", message.content)
client.run('Discord_BOT_TOKEN')
