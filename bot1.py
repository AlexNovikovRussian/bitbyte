from discord.ext import commands
import discord
import requests
import json
import datetime

bot = commands.Bot(command_prefix='$', description="Бот нашего сервера для получения информации о валюте (сколько 1 единица стоит в рублях)")

@bot.command(help="Курс в рублях", usage="[целевая валюта(USD)]", description="Отправляет курс указанной валюты в рублях")
async def rub(ctx, *args):

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name = "за рублём"))
    if len(args) == 0:
        rate = json.loads(requests.get("https://rubisintheass.firebaseio.com/RUB.json").text)["USD"]
        await ctx.send(embed=discord.Embed(title="USD", description="1 USD = " + str(rate) + " RUB", url="https://cash.rbc.ru/cash/converter.html?from=USD&to=RUR&sum=1&date=&rate=cbrf", timestamp=datetime.datetime.now()))
    else:
        arg1 = args[0].upper()
        rates = json.loads(requests.get("https://rubisintheass.firebaseio.com/RUB.json").text)
        try:
            rate = rates[arg1]
            await ctx.send(embed=discord.Embed(title=arg1, description="1 " + arg1 + " = " + str(rate) + " RUB", url="https://cash.rbc.ru/cash/converter.html?from=" + arg1 + "&to=RUR&sum=1&date=&rate=cbrf", timestamp=datetime.datetime.now()))
        except KeyError:
            await ctx.send(embed=discord.Embed(title="404 - " + arg1, description="Такая валюта не найдена", timestamp=datetime.datetime.now()))

bot.run("NzE5OTMxMjgzNzczMzI1MzEy.XvDFsw.rbk6t_M0WE6vCHXAnYKNjAXYdH4")
