import discord
from slash_commands import SetupCommands

bot = discord.Bot(debug_guilds=[997040506938867813])
setup_commands = SetupCommands(bot)
bot.add_cog(setup_commands)

@bot.event
async def on_ready(): # bot initialized correctly
    print(f"{bot.user} is ready and online!")

@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

bot.run('OTk3MDM4NjUwMjA4NTcxNDIy.Gg9v4W.vGEBzI4jh_jRyMCxnatKwAQF7ChhANDsRmOk6E')