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
                sql = "INSERT INTO `ServerInfo` VALUES (\'"+str(ctx.guild.id)+"\', \'"+str(channel.id)+"\', \""+ModuleStringHelper.moduleStringFiller("")+"\")"
                db_cursor.execute(sql)
                self.db_connection.commit()
                db_cursor.close()

                # Success Responses to log channel and channel called in
                await ctx.respond("Logging enabled for this server")
                await channel.send("Logs enabled in this channel")
            if(len(present)==1):
                db_cursor = self.db_connection.cursor()
                sql = "UPDATE `ServerInfo` SET log_id="+str(channel.id)+" WHERE guild_id="+str(ctx.guild.id)
                db_cursor.execute(sql)
                self.db_connection.commit()
                db_cursor.close()

                await ctx.respond("Log channel updated for this server")
                await channel.send("Logs enabled in this channel")
            self.reload_cache()
        except:
            print("Get fucked nerd") # WORKS
            
        return #TODO check database for existing channel, then rewrite

    @commands.has_permissions(administrator=True)
    @slash_command(description="Disables a specific logging module")
    async def enable_module(self, ctx, module: discord.Option(input_type=int, choices={
        # List of modules with index
        discord.OptionChoice("User Join", "0"),
        discord.OptionChoice("User Leave", "1"),
        discord.OptionChoice("Message Deleted", "2"),
        discord.OptionChoice("Message Edited", "3"),
        discord.OptionChoice("Nickname Changed", "4"),
        discord.OptionChoice("Purge Command Used", "5")
    })):
        guild_cache = await self.get_guild_cache(ctx.guild.id)

        moduleString = ''
        if module == str(0):
            moduleString = "1"+guild_cache[2][1:]
        else:
            for i in range(len(guild_cache[2])):
                if str(i) == module:
                    moduleString = guild_cache[2][:i]+'1'+guild_cache[2][i+1:]
        moduleString = ModuleStringHelper.moduleStringFiller(moduleString)

        db_cursor = self.db_connection.cursor()
        sql = "UPDATE `ServerInfo` SET modules='"+str(moduleString)+"' WHERE guild_id="+str(ctx.guild.id)
        db_cursor.execute(sql)
        self.db_connection.commit()
        db_cursor.close()

        await self.reload_cache()
        await ctx.respond("Module enabled")

    @commands.has_permissions(administrator=True)
    @slash_command(description="Disables a specific logging module")
    async def disable_module(self, ctx, module: discord.Option(input_type=int, choices={
        # List of modules with index
        discord.OptionChoice("User Join", "0"),
        discord.OptionChoice("User Leave", "1"),
        discord.OptionChoice("Message Deleted", "2"),
        discord.OptionChoice("Message Edited", "3"),
        discord.OptionChoice("Nickname Changed", "4"),
        discord.OptionChoice("Purge Command Used", "5")
        })):
        guild_cache = await self.get_guild_cache(ctx.guild.id)

        moduleString = ''
        if module == str(0):
            moduleString = '0'+guild_cache[2][1:]
        else:
            for i in range(len(guild_cache[2])):
                if str(i) == module:
                    moduleString = guild_cache[2][:i]+'0'+guild_cache[2][i+1:]
        moduleString = ModuleStringHelper.moduleStringFiller(moduleString)

        db_cursor = self.db_connection.cursor()
        sql = "UPDATE `ServerInfo` SET modules='"+str(moduleString)+"' WHERE guild_id="+str(ctx.guild.id)
        db_cursor.execute(sql)
        self.db_connection.commit()
        db_cursor.close()

        await self.reload_cache()
        await ctx.respond("Module disabled")

    async def get_guild_cache(self, ctx):
        for x in self.bot.local_db_cache:
            if x[0] == ctx:
                return x

    async def reload_cache(self):
        db_cursor = self.db_connection.cursor()
        db_cursor.execute("SELECT * FROM ServerInfo")
        result = db_cursor.fetchall()
        db_cursor.close()
        self.bot.local_db_cache.clear()
        for x in result:
            self.bot.local_db_cache.append(x)
    
    
class ModuleStringHelper:
    def moduleStringFiller(mods):
        for i in range(0, 255-len(mods)):
            mods+="0"
        return mods




    # BoolString module order
    #   1  deleted messages
    #   2  edited messages
    #   3  user join
    #   4  user leave
    #   5  purge
    #   6  nickname changed
    #   7  vc join
    #   8  vc leave
    #   9  repost deleted videos
    #   10 
