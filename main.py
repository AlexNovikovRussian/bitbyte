from discord.ext import commands
import discord
from pyowm.owm import OWM
import pyowm
from pyowm.utils.config import get_default_config
import requests
import json
import datetime


config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('d5cefe4e77e8e08ca203715b718cddde', config_dict)
mgr = owm.weather_manager()

bot = commands.Bot(command_prefix='%', description="Бот нашего сервера для разных приколов с написанием текста")

@bot.command(help="Делает шрифт ВоТ тАкИм", usage="[исходный текст]", description="", aliases=["сгзвщ", "капдо"])
async def cupdo(ctx, *args):
    string = ""
    exstring=""
    is_up=False
    for st in args:
        string +=st+" "
    
    for i in list(string):
        if i == " ":
            exstring += " "
            continue
        if is_up:
            exstring += i.lower()
            is_up = not is_up
        else:
            exstring += i.upper()
            is_up= not is_up
    await ctx.send(content=exstring)

@bot.command(help="", description="", aliases=["погода", "Погода", "цуерук"])
async def weather(ctx, *args):
    try:
        weather = mgr.weather_at_place(args[0]).weather
    except pyowm.commons.exceptions.NotFoundError:
        await ctx.send("Указанного Вами города/места не найдено")
        return
    temp = weather.temperature("celsius")
    print(temp)
    await ctx.send("Температура: " + str(temp["temp"]) + "\nМинимальная температура: " + str(temp["temp_min"]) + "\nМаксимальная температура: " + str(temp["temp_max"]) + "\nОщущается как: " + str(temp["feels_like"]))

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
            
    

bot.run("NzY4MDI4Mzk5MjEzNDc3ODkw.X46gLw.xiXUtgD8nmLJPNUP4YY2_r_goTc")
 
