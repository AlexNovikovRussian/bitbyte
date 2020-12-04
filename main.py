# from discord.ext import commands
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

TARGET = 3
PREFIX = "%"

mute_nick = None
mute_msg = None
muting = False
mute_reacts = [0,0]

class Bot(discord.Client):
    async def on_ready(self):
        print("Bot started!")
    
    async def on_message(self, message):
        args = message.content.split(" ")
        args.remove(args[0])
        if message.content.startswith(PREFIX+"cupdo" or PREFIX+"сгзвщ" or PREFIX+"капдо"):
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
            await message.delete()
            #await ctx.send(content="From {0}({1})\n{2}".format(ctx.message.author.display_name, ctx.message.author, exstring))
            await message.channel.send(embed=discord.Embed(description=exstring).set_author(name="{0}({1})".format(message.author.display_name, message.author),icon_url=message.author.avatar_url))
        
        elif message.content.startswith(PREFIX+"погода" or PREFIX+"пагода" or PREFIX+"цуферук" or PREFIX+"weather"):
            try:
                weather = mgr.weather_at_place(args[0]).weather
            except:
                await message.channel.send("Указанного Вами города/места не найдено")
                return
            temp = weather.temperature("celsius")
            print(temp)
            await message.channel.send("Температура: " + str(temp["temp"]) + "\nМинимальная температура: " + str(temp["temp_min"]) + "\nМаксимальная температура: " + str(temp["temp_max"]) + "\nОщущается как: " + str(temp["feels_like"]))
        
        elif message.content.startswith(PREFIX+"rub"):
            await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name = "за рублём"))
            if len(args) == 0:
                rate = json.loads(requests.get("https://rubisintheass.firebaseio.com/RUB.json").text)["USD"]
                await message.channel.send(embed=discord.Embed(title="USD", description="1 USD = " + str(rate) + " RUB", url="https://cash.rbc.ru/cash/converter.html?from=USD&to=RUR&sum=1&date=&rate=cbrf", timestamp=datetime.datetime.now()))
            else:
                arg1 = args[0].upper()
                rates = json.loads(requests.get("https://rubisintheass.firebaseio.com/RUB.json").text)
            try:
                rate = rates[arg1]
                await message.channel.send(embed=discord.Embed(title=arg1, description="1 " + arg1 + " = " + str(rate) + " RUB", url="https://cash.rbc.ru/cash/converter.html?from=" + arg1 + "&to=RUR&sum=1&date=&rate=cbrf", timestamp=datetime.datetime.now()))
            except KeyError:
                await message.channel.send(embed=discord.Embed(title="404 - " + arg1, description="Такая валюта не найдена", timestamp=datetime.datetime.now()))

        elif message.content.startswith(PREFIX+"reverse"):
            string = ""
            for st in args:
                string +=st+" "
            
            string = list(string)
            string.reverse()
            ex = "".join(string)

            await message.delete()
            await message.channel.send(embed=discord.Embed(description=ex).set_author(name="{0}({1})".format(message.author.display_name, message.author),icon_url=message.author.avatar_url))
            
bot = Bot()
bot.run("NzY4MDI4Mzk5MjEzNDc3ODkw.X46gLw.xiXUtgD8nmLJPNUP4YY2_r_goTc")



