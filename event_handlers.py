import discord
from discord.ext import commands
from discord.commands import Option
import mysql.connector as  mysql

class ModuleListeners(commands.Cog):
    def __init__(self, bot, db_connection):
        self.bot = bot
        self.db_connection = db_connection

    