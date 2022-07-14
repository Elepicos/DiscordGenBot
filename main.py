import discord

class SafeHavenBot(discord.Client):
    
    async def on_ready(self):
        print("ready to start")