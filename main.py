from discord.ext import commands
import discord
from pyowm.owm import OWM
import pyowm
from pyowm.utils.config import get_default_config

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
        
            
    

bot.run("NzY4MDI4Mzk5MjEzNDc3ODkw.X46gLw.xiXUtgD8nmLJPNUP4YY2_r_goTc")
 
