import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class SetupCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    purge_desc="This command purges a given number of messages"
    @slash_command(description=purge_desc)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, quantity: discord.Option(int), user: discord.Option(discord.User, required = True, default = None)):
        res=""
        if user == None:
            await ctx.channel.purge(limit=quantity)
            res+=(f"purging {quantity} messages from the channel")
        else:
            await ctx.channel.purge(limit=quantity, check=lambda msg: msg.author == user)
            res+=(f"purging {quantity} messages from {user} in the channel")
        await ctx.respond(res)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You are not authorized to use this command")

