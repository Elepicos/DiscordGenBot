#general imports
import yaml
import discord

#command cog imports
from slash_commands import ModCommands

#import important data from yaml (token, db creds, etc)
def read_config():
    with open('config.yml') as f:
        config = yaml.safe_load(f)
    return config

config = read_config()

#database imports and init
import mysql.connector as  mysql

HOST = config["db_host"]
DATABASE = config["db_name"]
USER = config["db_user"]
PASSWORD = config["db_pass"]
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)


print("Connected to:", db_connection.get_server_info())

bot = discord.Bot(debug_guilds=[997040506938867813])
setup_commands = ModCommands(bot)
bot.add_cog(setup_commands)

@bot.event
async def on_ready(): # bot initialized correctly
    print(f"{bot.user} is ready and online!")

@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

bot.run(config["Token"])