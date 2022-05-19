import json, discord, os, threading, time, datetime, random
from discord.ext import commands

uptime=0
GREEN=0xAAF0D1
RED=0xFAA0A0
BLUE=0xA7C7E7

RESTRICTED_USERS = []

bot = commands.Bot("t.", activity=discord.Game(name="t.help"))
bot.remove_command('help')

user_info = json.load(open("user_info.json"))
quizzes = json.load(open("quizzes.json"))

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

def gen_unit_quiz(unit):
	lessons = quizzes[unit]
	questions = []
	for lesson in list(lessons.keys()):questions += lessons[lesson]
	return questions

@bot.command(name="help")
async def command_help(ctx):
	file = open("help.txt")
	content = file.readlines();
	file.close()
	embed = discord.Embed(title=f"{bot.user.display_name} Commands", description=f"List of usable commands for {bot.user.display_name}", color=BLUE)
	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url=bot.user.avatar_url)
	for line in content:
		sections = line.split(" - ")
		title = sections[0]
		message = sections[1]
		embed.add_field(name=title, value=message)

	programmers_role = discord.utils.get(ctx.guild.roles, name="Programmers")
	mod_role = discord.utils.get(ctx.guild.roles, name="Mods")
	if programmers_role in ctx.author.roles or mod_role in ctx.author.roles:
		embed.add_field(name="t.configure", value=f"Allows the user to configure the behavior of {bot.user.display_name}.")
		embed.add_field(name="t.uptime", value=f"Allows the user to see the up-time of {bot.user.display_name}.")
	embed.set_footer(text=f"Requested by '{ctx.author}'")
	await ctx.send(embed=embed)

@bot.command(name="register")
async def command_register(ctx):
	embed = None
	if str(ctx.author.id) in user_info:embed = discord.Embed(title=ctx.author.display_name, description="You already have an account! Use t.info to see your info!", color=RED)
	else:
		embed = discord.Embed(title=ctx.author.display_name, description="Created your account! Use t.info to see your info!", color=GREEN)
		user_info[str(ctx.author.id)] = {}
		user_info[str(ctx.author.id)]["Koinsu"] = 0
		user_info[str(ctx.author.id)]["Correct Questions"] = 0
		user_info[str(ctx.author.id)]["Incorrect Questions"] = 0
		user_info[str(ctx.author.id)]["Quizzes Taken"] = 0
		user_info[str(ctx.author.id)]["Unit Quizzes Taken"] = 0
		user_info[str(ctx.author.id)]["Grade"] = "0%"
		user_info[str(ctx.author.id)]["Units Completed"] = []
		json.dump(user_info, open("user_info.json", "w"))
	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url=bot.user.avatar_url)
	embed.set_footer(text=f"Requested by '{ctx.author}'")
	await ctx.send(embed=embed)

@bot.command(name="quiz")
async def command_quiz(ctx, *, unit_and_lesson=""):
	questions = None
	sections = unit_and_lesson.split()
	unit = sections[0]
	lesson = sections[1]
	if str(unit) in quizzes:
		if str(lesson) in quizzes[str(unit)]:questions = quizzes[str(unit)][str(lesson)]
		else:
			lesson = "unit"
			questions = gen_unit_quiz(unit)
	else:
		prev_unit = unit
		if(len(user_info[str(ctx.author.id)]["Units Completed"]) == 0):unit="1"
		else:unit = random.choice(user_info[str(ctx.author.id)]["Units Completed"])
		if str(lesson) in quizzes[str(unit)]:questions = quizzes[str(unit)][str(lesson)]
		elif str(prev_unit) in quizzes[unit]:
			lesson = prev_unit
			questions = quizzes[str(unit)][str(prev_unit)]
		else:
			lesson = "unit"
			questions = gen_unit_quiz(unit)
	if lesson=="unit":embed = discord.Embed(title=f"Started a quiz for Unit {unit}!", description=f"This is the unit quiz for Unit {unit}!", color=BLUE)
	else:embed = discord.Embed(title=f"Started a quiz for Unit {unit}!", description=f"This is quiz '{lesson}' for Unit {unit}!", color=BLUE)
	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url=bot.user.avatar_url)
	embed.set_footer(text=f"Requested by '{ctx.author}'")
	await ctx.send(embed=embed)

@bot.command(name="info")
async def command_info(ctx):
	if str(ctx.author.id) in user_info:
		embed = discord.Embed(title=ctx.author.display_name, description="This is all your user info!", color=GREEN)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url=bot.user.avatar_url)
		embed.set_footer(text=f"Requested by '{ctx.author}'")
		embed.add_field(name="Koinsu", value=user_info[str(ctx.author.id)]["Koinsu"])
		embed.add_field(name="Correct Questions", value=user_info[str(ctx.author.id)]["Correct Questions"])
		embed.add_field(name="Incorrect Questions", value=user_info[str(ctx.author.id)]["Incorrect Questions"])
		embed.add_field(name="Quizzes Taken", value=user_info[str(ctx.author.id)]["Quizzes Taken"])
		embed.add_field(name="Unit Quizzes Taken", value=user_info[str(ctx.author.id)]["Unit Quizzes Taken"])
		if(len(user_info[str(ctx.author.id)]["Units Completed"]) == 0):embed.add_field(name="Units Completed", value="No Units Completed")
		else:embed.add_field(name="Units Completed", value=', '.join(user_info[str(ctx.author.id)]["Units Completed"]))
		embed.add_field(name="Grade", value=user_info[str(ctx.author.id)]["Grade"])
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
@commands.has_any_role("Programmers", "Mods")
async def command_configure(ctx):pass

@bot.event
async def on_message(message):
	if message.author == bot.user:return
	if(not message.author.id in RESTRICTED_USERS):await bot.process_commands(message)

@bot.event
async def on_ready():
	print(f"Logged in as '{bot.user}' at {datetime.datetime.now().strftime('%d/%m/%Y on %H:%M:%S')}!")
	uptime_thread = threading.Thread(target=tick_uptime)
	uptime_thread.start()

bot.run(os.environ['DISCORD_BOT_ID'])