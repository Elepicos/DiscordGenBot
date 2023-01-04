import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import mysql.connector as  mysql

class ModCommands(commands.Cog):
    def __init__(self, bot, db_connection):
        self.bot = bot
        self.db_connection = db_connection

    purge_desc="This command purges a given number of messages"
    @slash_command(description=purge_desc)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, quantity: discord.Option(int), user: discord.Option(discord.User, required = True, default = None)):
        res=""
        msg = []
        if user == None:
            await ctx.channel.purge(limit=quantity)
            res+=(f"purging {quantity} messages from the channel")
            print(f"purging {quantity} messages from {ctx.channel}")
        else:
            async for m in ctx.channel.history():
                if len(msg) == quantity:
                    break
                
                if m.author == user:
                    msg.append(m)
            await ctx.channel.delete_messages(msg)
            #await ctx.channel.purge(limit=quantity, check=lambda msg: msg.author == user)
            res+=(f"purging {quantity} messages from {user} in the channel")
            print(f"purging {quantity} messages from {user} in {ctx.channel}")
        await ctx.respond(res)

    #purge error handling
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You are not authorized to use this command")
        elif isinstance(error, discord.ClientException):
            await ctx.respond("Messages could not be deleted")

class SetupCommands(commands.Cog):
    def __init__(self, bot, db_connection):
        self.bot = bot
        self.db_connection = db_connection

    @slash_command(name="setlogchannel", description="Set main channel for server logs")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel: discord.Option(discord.TextChannel, required = True, default = None)):
        try:

            # Check for existing guild entry in database
            checkDbForEntry = "SELECT * FROM `ServerInfo` WHERE guild_id="+str(ctx.guild.id)
            checkDb_cursor = self.db_connection.cursor()
            checkDb_cursor.execute(checkDbForEntry)
            present = checkDb_cursor.fetchall()
            checkDb_cursor.close()

            # If no entry found, insert new entry with NULL modules enabled
            if(len(present)==0):
                db_cursor = self.db_connection.cursor()
                sql = "INSERT INTO `ServerInfo` VALUES (\'"+str(ctx.guild.id)+"\', \'"+str(channel.id)+"\', NULL)"
                db_cursor.execute(sql)
                self.db_connection.commit()

                # Success Responses to log channel and channel called in
                await ctx.respond("Logging enabled for this server")
                await channel.send("Logs enabled in this channel")
            if(len(present)==1):
                db_cursor = self.db_connection.cursor()
                sql = "UPDATE `ServerInfo` SET log_id="+str(channel.id)+" WHERE guild_id="+str(ctx.guild.id)
                db_cursor.execute(sql)
                self.db_connection.commit()

                await ctx.respond("Log channel updated for this server")
                await channel.send("Logs enabled in this channel")
            
        except:
            print("Get fucked nerd") # WORKS
            
        return #TODO check database for existing channel, then rewrite

    @commands.has_permissions(administrator=True)
    @slash_command(description="Disables a specific logging module")
    async def enable_module(self, ctx, module: discord.Option(input_type=str)):
        length = len(module)
        for i in range(0, 255-length):
            module+="0"
        print(len(module))
        return #TODO finish setting up option for choices of module

    @commands.has_permissions(administrator=True)
    @slash_command(description="Disables a specific logging module")
    async def disable_module(self, ctx, module: discord.Option(input_type=str)):
        return #TODO finish setting up option for choices of module
    
    




    # BoolString module order
    #   1  deleted messages
    #   2  edited messages
    #   3  user join
    #   4  user leave
    #   5  purge
    #   6  nickname changed
    #   7  vc join
    #   8  vc leave
    #   9  mentions minecraft
    #   10 repost deleted videos
