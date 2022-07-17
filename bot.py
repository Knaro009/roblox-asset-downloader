import discord
import requests
import os
from discord.ext import commands
from time import sleep

token = "" # discord bot token not user token
# really messy and does not work with linux idk y
client = commands.Bot(command_prefix= "!")

def get_template(id):
    if not id.isdigit():
        return "ID is not a digit."
    res = requests.get(f"https://assetdelivery.roblox.com/v1/assetId/{id}")
    res = res.json()
    if not res["location"]: 
        return 'res["location"] does not exist.'
    res2 = requests.get(res["location"]).text
    if "<roblox xmlns:xmime=" not in res2:
        return '"<roblox xmlns:xmime=" not in res2.text.'
    assetid = res2.split("<url>http://www.roblox.com/asset/?id=")
    assetid = assetid[1].split("<")[0]
    assetclass = res2.split('<Item class="')
    assetclass = assetclass[1].split('" referent=')[0]
    res3 = requests.get(f"https://assetdelivery.roblox.com/v1/asset/?id={assetid}")
    template = open(f"{id}.png", "wb")
    template.write(res3.content)
    template.close()
    return os.path.realpath(template.name), assetclass

@client.command()
async def gt(ctx, inp):
    id = ""
    if inp.isdigit():
        id = inp
    elif "/catalog/" in inp:
        q = inp.split("/")
        for v in q:
            if v.isdigit():
                id = v
                break
    else:
        await ctx.send("Error. Please report to Rea.")
    templatepath, assetclass = get_template(id)
    if "\\" in templatepath:
        embed=discord.Embed(title=f"Template", color=0xf5cef7)
        embed.add_field(name="Asset Type", value=assetclass, inline=True)
        embed.set_footer(text="Image size should be 585x559")
        file = discord.File(templatepath, filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(embed=embed, file=file)
        sleep(1)
        os.remove(templatepath)

    
client.run(token)    




"""
f"https://assetdelivery.roblox.com/v1/assetId/{
# q = requests.get(url)
https://assetdelivery.roblox.com/v1/assetId/6701856667
https://www.roblox.com/catalog/6701856667/white
await ctx.send(url)

embed=discord.Embed(title="ASSETNAME - by USERNAME", color=0xf5cef7)
embed.add_field(name="Asset Type", value="ASSETTYPE", inline=True)
embed.set_footer(text="Image size should be 585x559")
await ctx.send(embed=embed)
"""
