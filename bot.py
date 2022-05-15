import json, discord, os, threading, time, datetime
from discord.ext import commands

uptime=0
GREEN=0xAAF0D1
RED=0xFAA0A0
BLUE=0xA7C7E7

bot = commands.Bot("t.", activity=discord.Game(name="t.help"))
bot.remove_command('help')

user_info = json.load(open("user_info.json"))

def tick_uptime():
	global uptime
	while True:
		uptime+=0.01
		time.sleep(0.01)

def format_timedelta(delta):
    seconds = int(delta.total_seconds())
    secs_in_a_day = 86400
    secs_in_a_hour = 3600
    secs_in_a_min = 60
    days, seconds = divmod(seconds, secs_in_a_day)
    hours, seconds = divmod(seconds, secs_in_a_hour)
    minutes, seconds = divmod(seconds, secs_in_a_min)
    time_fmt = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    if days > 0:
        suffix = "s" if days > 1 else ""
        return f"{days} day{suffix} {time_fmt}"
    return time_fmt

@bot.command(name="help")
async def command_help(ctx):pass

@bot.command(name="register")
async def command_register(ctx):
	embed = None
	if ctx.author.id in user_info:embed = discord.Embed(title=ctx.author.display_name, description="You already have an account! Use t.info to see your info!", color=RED)
	else:
		embed = discord.Embed(title=ctx.author.display_name, description="Created your account! Use t.info to see your info!", color=GREEN)
		user_info[ctx.author.id] = {}
		user_info[ctx.author.id]["Koinsu"] = 0
		user_info[ctx.author.id]["Correct Questions"] = 0
		user_info[ctx.author.id]["Incorrect Questions"] = 0
		user_info[ctx.author.id]["Quizzes Taken"] = 0
		user_info[ctx.author.id]["Unit Quizzes Taken"] = 0
		user_info[ctx.author.id]["Grade"] = "0%"
		json.dump(user_info, open("user_info.json", "w"))
	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url=bot.user.avatar_url)
	embed.set_footer(text=f"Requested by '{ctx.author}'")
	await ctx.send(embed=embed)

@bot.command(name="quiz")
async def command_quiz(ctx, unit, lesson):pass

@bot.command(name="info")
async def command_info(ctx):
	if ctx.author.id in user_info:
		embed = discord.Embed(title=ctx.author.display_name, description="This is all your user info!", color=GREEN)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url=bot.user.avatar_url)
		embed.set_footer(text=f"Requested by '{ctx.author}'")
		embed.add_field(name="Koinsu", value=user_info[ctx.author.id]["Koinsu"])
		embed.add_field(name="Correct Questions", value=user_info[ctx.author.id]["Correct Questions"])
		embed.add_field(name="Incorrect Questions", value=user_info[ctx.author.id]["Incorrect Questions"])
		embed.add_field(name="Quizzes Taken", value=user_info[ctx.author.id]["Quizzes Taken"])
		embed.add_field(name="Unit Quizzes Taken", value=user_info[ctx.author.id]["Unit Quizzes Taken"])
		embed.add_field(name="Grade", value=user_info[ctx.author.id]["Grade"])
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title=ctx.author.display_name, description = "You do not have an account, use t.register to create one!", color=RED)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url=bot.user.avatar_url)
		embed.set_footer(text=f"Requested by '{ctx.author}'")
		await ctx.send(embed=embed)

@bot.command(name="source")
async def command_source(ctx):
	embed = discord.Embed(title=f"{bot.user.display_name} Source code", url="https://github.com/Baskaradono/Nihongo-TA", description=f"{bot.user.display_name} source code on github!", color=BLUE)
	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url=bot.user.avatar_url)
	embed.set_footer(text=f"Requested by '{ctx.author}'")
	embed.add_field(name="Github Link", value="https://github.com/Baskaradono/Nihongo-TA")
	await ctx.send(embed=embed)

@bot.command(name="github")
async def command_github(ctx):await command_source(ctx)

@bot.command(name="uptime")
@commands.has_any_role("Programmers", "Mods")
async def command_uptime(ctx):
	global uptime
	embed = discord.Embed(title=f"{bot.user.display_name} Up-Time", description=f"{bot.user.display_name} has been up for {format_timedelta(datetime.timedelta(seconds=uptime))}", color=BLUE)
	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url=bot.user.avatar_url)
	embed.set_footer(text=f"Requested by '{ctx.author}'")
	await ctx.send(embed=embed)

@bot.command(name="configure")
@commands.has_any_role("Programmers", "Teachers", "Mods")
async def command_configure(ctx):pass

@bot.event
async def on_message(message):
	if message.author == bot.user:return
	await bot.process_commands(message)

@bot.event
async def on_ready():
	print(f"Logged in as '{bot.user}'!")
	uptime_thread = threading.Thread(target=tick_uptime)
	uptime_thread.start()

bot.run(os.environ['DISCORD_BOT_ID'])