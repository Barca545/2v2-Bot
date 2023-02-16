import gspread
import dotenv 
import discord
from discord.ext import commands, tasks
from discord.commands import Option 
import os
import re #delete
import string #delete

#dotenv In
dotenv.load_dotenv()

#Discord Bot Initiation
token = str(os.getenv("DISC_TOKEN"))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 

#Gspread Initation
gc = gspread.service_account(filename=r"C:\Users\jamar\Documents\Hobbies\Coding\2v2 Bot\v2-bot-374602-e64743327d13.json")
#gc = gspread.service_account('/home/jamari/2v2bot/v2-bot-374602-e64743327d13,json') #Deployment JSON

bot_database = gc.open_by_url('https://docs.google.com/spreadsheets/d/134T4caUqFHG3crrS_Rk9Z3ON5o6mc19tPt4kTm4R834') #Testing JSON 
Botlaners = bot_database.get_worksheet_by_id(0)
Supports = bot_database.get_worksheet_by_id(1953196714)
Tops = bot_database.get_worksheet_by_id(839126568)
Mids = bot_database.get_worksheet_by_id(431869411)


