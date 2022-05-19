import discord, os, sys
from discord.ext import commands

bot = commands.Bot("t.", activity=discord.Game(name="t.help"))
bot.remove_command('help')

@bot.command(name="help")
async def command_help(ctx, *, command=""):
	os.system("clear")
	import bot_commands
	await bot_commands.command_help(bot, ctx, command)
	if "bot_commands" in sys.modules:del sys.modules["bot_commands"]

@bot.command(name="register")
async def command_register(ctx):
	os.system("clear")
	import bot_commands
	await bot_commands.command_register(bot, ctx)
	if "bot_commands" in sys.modules:del sys.modules["bot_commands"]

@bot.command(name="quiz")
async def command_quiz(ctx, *, unit_and_lesson=""):
	os.system("clear")
	import bot_commands
	await bot_commands.command_quiz(bot, ctx, unit_and_lesson)
	if "bot_commands" in sys.modules:del sys.modules["bot_commands"]

@bot.command(name="info")
async def command_info(ctx):
	os.system("clear")
	import bot_commands
	await bot_commands.command_info(bot, ctx)
	if "bot_commands" in sys.modules:del sys.modules["bot_commands"]

@bot.command(name="source")
async def command_source(ctx):
	os.system("clear")
	import bot_commands
	await bot_commands.command_source(bot, ctx)
	if "bot_commands" in sys.modules:del sys.modules["bot_commands"]

@bot.command(name="github")
async def command_github(ctx):
	os.system("clear")
	import bot_commands
	await bot_commands.command_source(bot, ctx)
	if "bot_commands" in sys.modules:del sys.modules["bot_commands"]

@bot.event
async def on_message(message):
	os.system("clear")
	import bot_commands
	await bot_commands.on_message(bot, message)
	if "bot_commands" in sys.modules:del sys.modules["bot_commands"]

@bot.event
async def on_ready():
	os.system("clear")
	import bot_commands
	await bot_commands.on_ready(bot)
	if "bot_commands" in sys.modules:del sys.modules["bot_commands"]

bot.run(os.environ['DISCORD_BOT_ID'])