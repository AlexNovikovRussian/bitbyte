# from discord.ext import commands
import discord
from pyowm.owm import OWM
import pyowm
from pyowm.utils.config import get_default_config
import requests
import json
import datetime
from discord.utils import get
from os import environ as env


config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('d5cefe4e77e8e08ca203715b718cddde', config_dict)
mgr = owm.weather_manager()

TARGET = 3
PREFIX = "%"

class Voicing():
    def __init__(self, message,member,state):
        self.message = message
        self.member = member
        self.state = state
        self.positive_reactions = 0
        self.negative_reactions = 0


mute = Voicing(None,None,None)
unmute = Voicing(None,None,None)

class Bot(discord.Client):
    async def on_ready(self):
        print("Bot started!")
    
    async def on_message(self, message):
        args = message.content.split(" ")
        args.remove(args[0])
        if message.content.lower().startswith(PREFIX+"cupdo" or PREFIX+"сгзвщ" or PREFIX+"капдо"):
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
        
        elif message.content.lower().startswith(PREFIX+"погода" or PREFIX+"пагода" or PREFIX+"цуферук" or PREFIX+"weather"):
            try:
                weather = mgr.weather_at_place(args[0]).weather
            except:
                await message.channel.send("Указанного Вами города/места не найдено")
                return
            temp = weather.temperature("celsius")
            print(temp)
            await message.channel.send("Температура: " + str(temp["temp"]) + "\nМинимальная температура: " + str(temp["temp_min"]) + "\nМаксимальная температура: " + str(temp["temp_max"]) + "\nОщущается как: " + str(temp["feels_like"]))
        
        elif message.content.lower().startswith(PREFIX+"rub"):
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

        elif message.content.lower().startswith(PREFIX+"reverse"):
            string = ""
            for st in args:
                string +=st+" "
            
            string = list(string)
            string.reverse()
            ex = "".join(string)

            await message.delete()
            await message.channel.send(embed=discord.Embed(description=ex).set_author(name="{0}({1})".format(message.author.display_name, message.author),icon_url=message.author.avatar_url))
        
        elif message.content.lower().startswith(PREFIX+"mute"):
            if mute.state == True:
                await message.channel.send("Процесс голосования уже запущен, завершите его для начала следущего")
                return
            mentions = message.mentions
            try:
                assert len(mentions) ==1
            except:
                await message.channel.send("Вы не указали пользователя")
                return
            
            mute.member = mentions[0]
            del mentions
            if mute.member.bot == True:
                await message.channel.send("Боты - это исчезающий вид, НЕ УБИВАЙТЕ БЕЗЗАЩИТНЫХ!")
                return
            if get(mute.member.guild.roles, name="банка") in mute.member.roles:
                await message.channel.send("Замутить замученного? Не справедливо!")
                return
            mute.message = await message.channel.send("Замутить **"+mute.member.display_name+"** Кто за, ставьте <:correct:784434578424725535>, если нет, то <:incorrect:714834242525331498>")
            mute.state = True
            await mute.message.add_reaction("<:correct:784434578424725535>")
            await mute.message.add_reaction("<:incorrect:714834242525331498>")
        
        elif message.content.lower().startswith(PREFIX+"unmute"):
            if unmute.state == True:
                await message.channel.send("Процесс голосования уже запущен, завершите его для начала следущего")
                return
            mentions = message.mentions
            try:
                assert len(mentions) ==1
            except:
                await message.channel.send("Вы не указали пользователя")
                return
            
            if not get(mentions[0].guild.roles, name="банка") in mentions[0].roles:
                await message.channel.send("Человек не замьючен")
                return
            unmute.member = mentions[0]
            del mentions

            unmute.message = await message.channel.send("Размутить **"+unmute.member.display_name+"** Кто за, ставьте <:correct:784434578424725535>, если нет, то <:incorrect:714834242525331498>")
            unmute.state = True
            await unmute.message.add_reaction("<:correct:784434578424725535>")
            await unmute.message.add_reaction("<:incorrect:714834242525331498>")

    async def on_reaction_add(self,reaction, user):
        if reaction.message == mute.message:
            if str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/784434578424725535.png": #positive
                mute.positive_reactions += 1
                
                if mute.positive_reactions >= TARGET:
                    await mute.message.delete()

                    role_ids = [str(r.id) for r in mute.member.roles]
                    rls = ":".join(role_ids)
                    req = {str(mute.member.id): rls}
                    requests.patch("https://rubisintheass.firebaseio.com/MUTES.json", data=json.dumps(req))

                    await mute.member.edit(roles=[])

                    role = get(reaction.message.guild.roles, name="банка")
                    await mute.member.add_roles(role, reason="голосование")
                    mute.member = None
                    mute.message = None
                    mute.state = False
                    mute.positive_reactions = 0
                    mute.negative_reactions = 0
                    await reaction.message.channel.send("mute")
                
            elif str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/714834242525331498.png": #negative
                mute.negative_reactions += 1

                if mute.negative_reactions >= TARGET:
                    await mute.message.delete()
                    mute.member = None
                    mute.message = None
                    mute.state = False
                    mute.positive_reactions = 0
                    mute.negative_reactions = 0
                    await reaction.message.channel.send("no mute")
        elif reaction.message == unmute.message:
            if str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/784434578424725535.png": #positive
                unmute.positive_reactions += 1
                
                if unmute.positive_reactions >= TARGET:
                    await unmute.message.delete()

                    user = json.loads(requests.get("https://rubisintheass.firebaseio.com/MUTES.json").text)[str(unmute.member.id)]

                    rls = user.split(":")
                    roles = [get(unmute.member.guild.roles, id=int(r)) for r in rls]

                    await unmute.member.edit(roles=roles)

                    unmute.member = None
                    unmute.message = None
                    unmute.state = False
                    unmute.positive_reactions = 0
                    unmute.negative_reactions = 0
                    await reaction.message.channel.send("unmute")
                
            elif str(reaction.emoji.url) == "https://cdn.discordapp.com/emojis/714834242525331498.png": #negative
                unmute.negative_reactions += 1

                if unmute.negative_reactions >= TARGET:
                    await unmute.message.delete()
                    unmute.member = None
                    unmute.message = None
                    unmute.state = False
                    unmute.positive_reactions = 0
                    unmute.negative_reactions = 0
                    await reaction.message.channel.send("no unmute")

bot = Bot()
bot.run(env["DSICORD_TOKEN"])



