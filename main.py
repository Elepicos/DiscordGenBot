#general imports
import yaml
import discord

#command cog imports
from slash_commands import ModCommands
from slash_commands import SetupCommands
from event_handlers import ModuleListeners

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

#initialize bot
bot = discord.Bot(debug_guilds=[997040506938867813])

#add command cogs from commands file
mod_commands = ModCommands(bot, db_connection)
bot.add_cog(mod_commands)
setup_commands = SetupCommands(bot, db_connection)
bot.add_cog(setup_commands)
module_listeners = ModuleListeners(bot, db_connection)
bot.add_cog(module_listeners)

bot.local_db_cache = [("", "", "")]

@bot.event
async def on_ready(): # bot initialized correctly
    print(f"{bot.user} is ready and online!")
    reload_cache()
    #print(bot.local_db_cache) 
    #print(bot.local_db_cache[0][0])


#ping check command
@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    print(bot.local_db_cache)
    await ctx.respond(f"Pong! Latency is {bot.latency}")

def reload_cache():
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM ServerInfo")
    result = db_cursor.fetchall()
    db_cursor.close()
    bot.local_db_cache.clear()
    for x in result:
        bot.local_db_cache.append(x)

bot.run(config["Token"])